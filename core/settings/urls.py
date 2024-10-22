from rest_framework_nested.routers import DefaultRouter
from core.base.routers import register_model_routes
from . import views


app_name = "settings"

router = DefaultRouter()

city_router = register_model_routes(
    router,
    "cities",
    views.CityViewSet,
    {
        "zones": views.GeographicalZoneViewSet,
    },
    "city",
)

sub_region_router = register_model_routes(
    router,
    "sub-regions",
    views.SubRegionViewSet,
    {"zones": views.GeographicalZoneViewSet, "cities": views.CityViewSet},
    "sub_region",
)

region_router = register_model_routes(
    router,
    "regions",
    views.RegionViewSet,
    {
        "zones": views.GeographicalZoneViewSet,
        "sub-regions": (
            views.SubRegionViewSet,
            {"cities": views.CityViewSet},
            "sub_region",
        ),
        "cities": views.CityViewSet,
    },
    "region",
)


country_router = register_model_routes(
    router,
    "countries",
    views.CountryViewSet,
    {
        "zones": views.GeographicalZoneViewSet,
        "regions": (
            views.RegionViewSet,
            {
                "sub-regions": (
                    views.SubRegionViewSet,
                    {"cities": views.CityViewSet},
                    "sub_region",
                ),
                "cities": views.CityViewSet,
            },
            "region",
        ),
        "sub-regions": (
            views.SubRegionViewSet,
            {"cities": views.CityViewSet},
            "sub_region",
        ),
        "cities": views.CityViewSet,
    },
    "country",
)


router.register(r"zones", views.GeographicalZoneViewSet)
router.register(r"currencies", views.CurrencyViewSet)
router.register(r"seo", views.SEOSettingsViewSet)
router.register(r"general", views.GlobalSettingsViewSet, basename="globalsettings")
router.register(r"branches", views.BranchSettingsViewSet, basename="branchsettings")
router.register(r"users", views.UserSettingViewSet, basename="usersettings")
router.register(r"customers", views.CustomerSettingViewSet, basename="customersettings")
router.register(
    r"central-staffs", views.CentralSettingViewSet, basename="centralstaffssettings"
)
router.register(
    r"deliveries", views.DeliverySettingViewSet, basename="deliverysettings"
)
router.register(r"preparers", views.PreparerSettingViewSet, basename="preparersettings")
router.register(
    r"branch-staffs", views.StaffSettingViewSet, basename="branchstaffsettings"
)
router.register(
    r"delivering", views.DeliveringSettingViewSet, basename="deliveringsettings"
)
router.register(
    r"preparing", views.PreparingSettingViewSet, basename="preparingsettings"
)
router.register(r"managers", views.ManagerSettingViewSet, basename="managersettings")


urlpatterns = []
urlpatterns += router.urls
urlpatterns += city_router.urls
urlpatterns += sub_region_router.urls
urlpatterns += region_router.urls
urlpatterns += country_router.urls
