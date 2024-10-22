from math import ceil
from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response

from math import ceil
from rest_framework.pagination import (
    BasePagination,
    CursorPagination,
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.response import Response

class CustomPagination(BasePagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
    display_page_controls = True  # إضافة الخاصية

    def __init__(self):
        self.paginator = None
        self.request = None

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        if 'cursor' in request.query_params:
            self.paginator = CursorPagination()
            self.paginator.page_size = self.page_size
            self.paginator.cursor_query_param = 'cursor'
            self.paginator.page_size_query_param = self.page_size_query_param
            self.paginator.max_page_size = self.max_page_size
            return self.paginator.paginate_queryset(queryset, request, view)

        elif 'limit' in request.query_params or 'offset' in request.query_params:
            self.paginator = LimitOffsetPagination()
            self.paginator.default_limit = self.page_size
            self.paginator.limit_query_param = 'limit'
            self.paginator.offset_query_param = 'offset'
            self.paginator.max_limit = self.max_page_size
            return self.paginator.paginate_queryset(queryset, request, view)

        else:
            self.paginator = PageNumberPagination()
            self.paginator.page_size = self.page_size
            self.paginator.page_size_query_param = self.page_size_query_param
            self.paginator.max_page_size = self.max_page_size
            self.paginator.page_query_param = 'page'
            return self.paginator.paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if isinstance(self.paginator, CursorPagination):
            return Response({
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': data
            })
        elif isinstance(self.paginator, LimitOffsetPagination):
            total_items = self.paginator.count
            current = self.paginator.offset
            limit = self.paginator.get_limit(self.request)
            total_pages = ceil(total_items / limit) if limit else 1
            return Response({
                'count': total_items,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'total_pages': total_pages,
                'results': data,
                'current_page': current,
            })
        elif isinstance(self.paginator, PageNumberPagination):
            total_pages = self.paginator.page.paginator.num_pages
            current = self.paginator.page.number
            return Response({
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'current_page': current,
                'total_pages': total_pages,
                'results': data,
            })

    def get_results(self, data):  # إضافة الدالة
        """
        إرجاع قائمة النتائج لهذه الصفحة.
        """
        return data
