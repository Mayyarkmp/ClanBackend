from rest_framework import serializers
from .models import (
    Country,
    Region,
    SubRegion,
    City,
    Currency,
    GeographicalZone,
    GeneralSettings,
)
from core.base.serializers import SuperModelSerializer
from django.contrib.auth.models import Group, Permission
from .models.seo import SEOSettings
from ..media.models import Media
from django.apps import apps


class CountrySerializer(SuperModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class RegionSerializer(SuperModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class SubRegionSerializer(SuperModelSerializer):
    class Meta:
        model = SubRegion
        fields = "__all__"


class CitySerializer(SuperModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class GeographicalZoneSerializer(SuperModelSerializer):
    class Meta:
        model = GeographicalZone
        fields = "__all__"


class CurrencySerializer(SuperModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class SEOSettingsSerializer(SuperModelSerializer):
    image = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Media.objects.all(), allow_null=True
    )

    class Meta:
        model = SEOSettings
        fields = "__all__"


class GeneralSettingsSerializer(SuperModelSerializer):
    class Meta:
        model = GeneralSettings
        fields = "__all__"
