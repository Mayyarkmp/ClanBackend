from datetime import datetime
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import GenericAPIView
from core.base.pagination import CustomPagination
from customers.serializers import BrowsingKeySerializer, AnonymousCustomerSerializer
from products.models import Product
from .products.serializers import ProductSerializer
from .permissions import BrowsingKeyPermission
from .utils import CustomerUtils


class AnonymousCustomerView(APIView):
    def post(self, request):
        if request.COOKIES.get("fingerprint", None):
            response = Response(
                {"fingerprint": request.COOKIES.get("fingerprint")},
                status=status.HTTP_200_OK,
            )
            return response

        if request.session.get("fingerprint", None):
            response = Response(
                {"fingerprint": request.session.get("fingerprint")},
                status=status.HTTP_200_OK,
            )
            response.set_cookie("fingerprint", request.session.get("fingerprint"))
            return response

        serializer = AnonymousCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            request.session["fingerprint"] = serializer.data["fingerprint"]
            request.session.save()
            request.COOKIES["fingerprint"] = serializer.data["fingerprint"]
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.set_cookie("fingerprint", serializer.data["fingerprint"])
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateKeyBrowsingView(GenericAPIView):
    serializer_class = BrowsingKeySerializer

    def post(self, request):
        anonymous = CustomerUtils.get_anonymous_customer(request)

        if self.request.user.is_authenticated:
            request.data["customer"] = self.request.user.id

        if anonymous:
            request.data["anonymous"] = anonymous.id

        if not anonymous and not self.request.user.is_authenticated:
            return Response({"message": _("This request should be authenticated")})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.session["browsing_key"] = serializer.data["key"]
        return Response({"key": serializer.data["key"]})


class FavoriteViewSet(ViewSet):
    """
    ViewSet مستقل للتعامل مع المفضلات
    """

    def list(self, request):
        browsing_key = CustomerUtils.get_browsing_key(request)
        user = request.user
        favorites = []

        # جلب المفضلات للمستخدم سواء كان مسجلاً أو غير مسجل
        if user.is_authenticated:
            favorites = user.favorites.all()
        elif browsing_key:
            if browsing_key.anonymous:
                favorites = browsing_key.anonymous.favorites.all()
            if browsing_key.user:
                favorites = browsing_key.user.favorites.all()

        # استخدام التجزئة فقط في هذه الفيو
        paginator = CustomPagination()
        paginator.page_size = 10  # تحديد حجم الصفحة هنا
        paginated_favorites = paginator.paginate_queryset(favorites, request)

        # إرجاع البيانات المجزأة إذا كانت موجودة
        serializer = ProductSerializer(paginated_favorites, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        browsing_key = CustomerUtils.get_browsing_key(request)
        user = request.user
        product_id = request.data.get("product")

        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                if user.is_authenticated:
                    user.favorites.add(product)
                elif browsing_key:
                    if browsing_key.anonymous:
                        browsing_key.anonymous.favorites.add(product)
                    if browsing_key.user:
                        browsing_key.user.favorites.add(product)

                return Response(
                    {"message": "تم إضافة المنتج إلى المفضلات"},
                    status=status.HTTP_201_CREATED,
                )
            except Product.DoesNotExist:
                return Response(
                    {"message": "المنتج غير موجود"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"message": "يجب تحديد معرف المنتج"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None):
        browsing_key = CustomerUtils.get_browsing_key(request)
        user = request.user

        if pk:
            try:
                product = Product.objects.get(pk=pk)
                if user.is_authenticated:
                    user.favorites.remove(product)
                elif browsing_key:
                    if browsing_key.anonymous:
                        browsing_key.anonymous.favorites.remove(product)
                    if browsing_key.user:
                        browsing_key.user.favorites.remove(product)

                return Response(
                    {"message": "تم حذف المنتج من المفضلات"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except Product.DoesNotExist:
                return Response(
                    {"message": "المنتج غير موجود"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {"message": "يجب تحديد معرف المنتج"},
            status=status.HTTP_400_BAD_REQUEST,
        )
