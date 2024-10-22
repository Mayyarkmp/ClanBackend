from rest_framework import viewsets
from django.db.models import (
    Q,
    ForeignKey,
    ManyToManyField,
    OneToOneField,
    CharField,
    TextField,
    IntegerField,
    FloatField,
    DecimalField,
    ManyToManyRel,
    ManyToOneRel,
    ForeignObjectRel,
    OneToOneRel,
)
from rest_framework.response import Response
from rest_framework import status


from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

class MultiLookupMixin:
    """
    Mixin يسمح باستخدام أكثر من متغير للبحث في ModelViewSet.
    يجب تحديد المتغيرات في قائمة lookup_fields.
    """

    lookup_fields = ["pk"]

    def get_object(self):
        queryset = self.get_queryset()
        

        lookup_value = self.kwargs.get(self.lookup_field)  # الحصول على القيمة من URL

        # محاولة البحث في جميع الحقول المحددة
        for field in self.lookup_fields:
            try:
                # جلب الكائن بناءً على الحقل الحالي
                obj = get_object_or_404(queryset, **{field: lookup_value})
                return obj
            except (ValueError, queryset.model.DoesNotExist):
                continue

        # إذا لم يتم العثور على الكائن
        raise NotFound(f"Object with these identifiers ({self.lookup_fields}) not found.")


class FieldsMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        fields = self.request.query_params.get("fields", None)
        if fields:
            fields = fields.split(",")
            kwargs["fields"] = fields
        return super().get_serializer(*args, **kwargs)

    def filter_queryset_fields(self, queryset):
        fields = self.request.query_params.get("fields", None)
        if fields:
            fields = fields.split(",")
            queryset = queryset.only(*fields)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset_fields(queryset)


class SearchFilterOrderingMixin:
    def get_meta_option(self, option_name, default_value=[]):
        if hasattr(self.queryset, "model") and hasattr(
            self.queryset.model, "MetaOptions"
        ):
            return getattr(self.queryset.model.MetaOptions, option_name, default_value)
        return default_value

    def initialize_meta_fields(self):
        searchable_field_types = (
            CharField,
            TextField,
            IntegerField,
            FloatField,
            DecimalField,
        )
        fields = []
        model_fields = []
        if hasattr(self.queryset, "model"):
            fields = [
                f.name
                for f in self.queryset.model._meta.get_fields()
                if not f.is_relation
                and f.concrete
                and isinstance(f, searchable_field_types)
            ]
            model_fields = [f.name for f in self.queryset.model._meta.get_fields()]
        self.search_fields = self.get_meta_option("search_fields", fields)
        if "delayed" in model_fields:
            model_fields.remove("delayed")
        self.filterset_fields = self.get_meta_option("filterset_fields", model_fields)
        self.filter_fields = self.filterset_fields
        self.ordering_fields = model_fields

    def initialize_request(self, request, *args, **kwargs):
        self.initialize_meta_fields()
        return super().initialize_request(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response.data["available_fields"] = {
            "search_fields": self.search_fields,
            "filterset_fields": self.filterset_fields,
            "ordering_fields": self.ordering_fields,
        }
        return response


class NestedViewSetQuerySet:
    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            if self.parent_lookup_kwargs:
                for param, lookups in self.parent_lookup_kwargs.items():

                    value = self.kwargs.get(param)
                    if value:
                        q = Q()
                        if isinstance(lookups, str):
                            q |= Q(**{lookups: value})
                        elif isinstance(lookups, list or tuple):
                            for lookup in lookups:
                                q |= Q(**{lookup: value})
                        elif isinstance(lookups, dict):
                            query = lookups.get("query", None)
                            if query:
                                if isinstance(query, str):
                                    q |= Q(**{query: value})
                                elif isinstance(query, list or tuple):
                                    for lookup in query:
                                        q |= Q(**{lookup: value})
                        queryset = queryset.filter(q)
                return queryset.distinct()
        except AttributeError as e:
            print(e)
            return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.parent_lookup_kwargs:
            for param, lookups in self.parent_lookup_kwargs.items():
                value = self.kwargs.get(param)
                if value:
                    related_name = None
                    if isinstance(lookups, dict):
                        related_name = lookups.get("related_name", None)
                    elif isinstance(lookups, str):
                        related_name = lookups.split("__")[0]

                    elif isinstance(lookups, list or tuple):
                        pass
                    if related_name:
                        if hasattr(instance, related_name):
                            related_field = getattr(instance, related_name, None)
                            if hasattr(related_field, "remove"):
                                related_objects = related_field.filter(pk=value)
                                if related_objects.exists():
                                    related_field.remove(related_objects.first())
                                    return Response(status=status.HTTP_204_NO_CONTENT)
                            if isinstance(related_field, ManyToManyField):
                                related_objects = related_field.filter(pk=value)
                                if related_objects.exists():
                                    related_field.remove(related_objects.first())
                                    return Response(status=status.HTTP_204_NO_CONTENT)
                            elif isinstance(related_field, ForeignKey):
                                setattr(instance, related_name, None)
                                instance.save()
                                return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)


class SuperViewSet(
    FieldsMixin, SearchFilterOrderingMixin, NestedViewSetQuerySet, viewsets.ViewSet
):
    pass


class SuperGenericViewSet(
    FieldsMixin,
    SearchFilterOrderingMixin,
    NestedViewSetQuerySet,
    viewsets.GenericViewSet,
):
    pass


class SuperModelViewSet(
    FieldsMixin, SearchFilterOrderingMixin, NestedViewSetQuerySet,MultiLookupMixin, viewsets.ModelViewSet
):
    pass


class SuperReadOnlyModelViewSet(
    FieldsMixin,
    SearchFilterOrderingMixin,
    NestedViewSetQuerySet,
    MultiLookupMixin,
    viewsets.ReadOnlyModelViewSet,
):
    pass
