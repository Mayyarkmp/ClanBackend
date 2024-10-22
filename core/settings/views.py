from .models import (
    Country,
    Region,
    SubRegion,
    City,
    Currency,
    GeographicalZone,
    SEOSettings,
    GeneralSettings,
)
from .serializers import (
    CountrySerializer,
    RegionSerializer,
    SubRegionSerializer,
    CitySerializer,
    CurrencySerializer,
    GeographicalZoneSerializer,
    SEOSettingsSerializer,
    GeneralSettingsSerializer,
)
from core.base.viewsets import SuperModelViewSet


class CountryViewSet(SuperModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    parent_lookup_kwargs = {
        "region_pk": ["regions__pk"],
        "sub_region_pk": ["sub_regions__pk"],
        "city_pk": ["cities__pk"],
    }


class RegionViewSet(SuperModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    parent_lookup_kwargs = {
        "country_pk": "country__pk",
        "sub_region_pk": "sub_regions__pk",
        "city_pk": "cities__pk",
    }


class SubRegionViewSet(SuperModelViewSet):
    serializer_class = SubRegionSerializer
    queryset = SubRegion.objects.all()
    parent_lookup_kwargs = {
        "country_pk": "country__pk",
        "region_pk": "region__pk",
        "city_pk": "cities__pk",
    }


class GeographicalZoneViewSet(SuperModelViewSet):
    serializer_class = GeographicalZoneSerializer
    queryset = GeographicalZone.objects.all()
    parent_lookup_kwargs = {
        "country_pk": "country__pk",
        "region_pk": "region__pk",
        "sub_region_pk": "subregion__pk",
        "city_pk": "city__pk",
    }


class CityViewSet(SuperModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    parent_lookup_kwargs = {
        "country_pk": "country__pk",
        "region_pk": "region__pk",
        "sub_region_pk": "subregion__pk",
    }


class CurrencyViewSet(SuperModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class SEOSettingsViewSet(SuperModelViewSet):
    queryset = SEOSettings.objects.all()
    serializer_class = SEOSettingsSerializer


class GlobalSettingsViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.GLOBAL)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.GLOBAL
        return super().create(request, *args, **kwargs)


class BranchSettingsViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.BRANCH)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.BRANCH
        return super().create(request, *args, **kwargs)


class UserSettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.USER)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.USER
        return super().create(request, *args, **kwargs)


class CustomerSettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.CUSTOMER)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.CUSTOMER
        return super().create(request, *args, **kwargs)


class CentralSettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.CENTRAL)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.CENTRAL
        return super().create(request, *args, **kwargs)


class DeliverySettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.DELIVERY)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.DELIVERY
        return super().create(request, *args, **kwargs)


class PreparerSettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.PREPARER)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.PREPARER
        return super().create(request, *args, **kwargs)


class StaffSettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.STAFF)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.STAFF
        return super().create(request, *args, **kwargs)


class DeliveringSettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.DELIVERING)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.DELIVERING
        return super().create(request, *args, **kwargs)


class PreparingSettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.PREPARING)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.PREPARING
        return super().create(request, *args, **kwargs)


class ManagerSettingViewSet(SuperModelViewSet):
    queryset = GeneralSettings.objects.filter(type=GeneralSettings.Type.MANAGER)
    serializer_class = GeneralSettingsSerializer

    def create(self, request, *args, **kwargs):
        request.data["type"] = GeneralSettings.Type.MANAGER
        return super().create(request, *args, **kwargs)
