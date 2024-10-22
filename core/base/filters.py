from django.db.models import ForeignKey
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from thefuzz import process
from django_filters import CharFilter

from django_filters import rest_framework as filters
from django.contrib.postgres.fields import ArrayField


class ArrayFilter(filters.BaseCSVFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        lookup = f"{self.field_name}__contains"
        return qs.filter(**{lookup: value})


class CustomOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):

        params = request.query_params.get(self.ordering_param)

        if params:
            fields = [param.strip() for param in params.split(",")]
            mapped_fields = []
            models_fields = queryset.model._meta.get_fields()
            fields_names = [field.name for field in models_fields]

            for field in fields:
                descending = field.startswith("-")
                field_name = field.lstrip("-")
                mapped_field = field_name

                if field_name not in fields_names and "__" not in field_name:
                    if hasattr(queryset.model, "_parler_meta"):
                        if field in queryset.model._parler_meta.get_translated_fields():
                            mapped_field = f"translations__{field_name}"

                        else:
                            closest_match, similarity = process.extractOne(
                                field_name, fields_names
                            )
                            if closest_match:
                                mapped_field = closest_match

                    else:
                        closest_match, similarity = process.extractOne(
                            field_name, fields_names
                        )
                        if closest_match:
                            mapped_field = closest_match

                if descending:
                    mapped_field = "-" + mapped_field
                mapped_fields.append(mapped_field)
            return mapped_fields
        return super().get_ordering(request, queryset, view)


class CustomDjangoFilterBackend(DjangoFilterBackend):
    def get_filterset(self, request, queryset, view):
        filterset_class = self.get_filterset_class(view, queryset)
        if filterset_class:
            data = request.query_params.copy()
            field_mapping = getattr(view, "field_mapping", {})
            new_data = {}
            for param, value in data.items():
                components = param.split("__")
                base_field = components[0]
                lookup = "__".join(components[1:])
                print(lookup)

                if lookup:
                    lookup = "__" + lookup
                else:
                    lookup = ""

                mapped_field = field_mapping.get(base_field, base_field)
                if hasattr(view.queryset.model, base_field) and isinstance(
                    view.queryset.model._meta.get_field(base_field), ForeignKey
                ):
                    mapped_field = field_mapping.get(base_field, f"{base_field}__name")
                actual_param = mapped_field + lookup
                new_data[actual_param] = value
            return filterset_class(new_data, queryset=queryset, request=request)
        return None


class CustomSearchFilter(SearchFilter):
    lookup_prefixes = {
        "^": "istartswith",
        "=": "icontains",
        "@": "search",
        "$": "iregex",
    }


class JSONFilter(CharFilter):
    def filter(self, qs, value):
        print(value)
        if value not in [None, ""]:
            lookup = f"delayed__contains"
            return qs.filter(**{lookup: value})
        return qs
