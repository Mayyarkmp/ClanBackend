from rest_framework_nested import routers
from django.urls import path, include
from core.base.routers import register_model_routes
from branches.views import (
    BranchViewSet,
    BranchServiceZoneViewSet,
    DeliveryTimeSlotViewSet,
)
from branches.products.views import (
    PricingGroupViewSet,
    ProductPriceViewSet,
    ProductQuantityViewSet,
    ShelfViewSet,
    SubShelfViewSet,
    PrimaryShelfViewSet,
    ProductViewSet,
    ProductChangeStateRequestViewSet,
    ProductTransferRequestViewSet,
    ProductSupplyRequestViewSet,
)
from branches.users.views import (
    ManagerViewSet,
    DeliveryViewSet,
    PreparerViewSet,
    StaffViewSet,
)
from orders.views import OrderViewSet
from branches.settings.views import BranchSettingsViewSet as SettingsViewSet


app_name = "branches"

router = routers.DefaultRouter()
branch_router = register_model_routes(
    router,
    "",
    BranchViewSet,
    {
        # "settings": SettingsViewSet,
        "zones": BranchServiceZoneViewSet,
        "delivery-time-slots": DeliveryTimeSlotViewSet,
        "manager": ManagerViewSet,
        "deliveries": DeliveryViewSet,
        "preparers": PreparerViewSet,
        "staffs": StaffViewSet,
        "orders": OrderViewSet,
        "products": (
            ProductViewSet,
            {
                "prices": ProductPriceViewSet,
                "quantities": ProductQuantityViewSet,
            },
            "product",
        ),
        "shelves/primary": PrimaryShelfViewSet,
        "shelves/sub": SubShelfViewSet,
        "shelves": ShelfViewSet,
        "supply_requests": ProductSupplyRequestViewSet,
        "transfer_requests": ProductTransferRequestViewSet,
        "change_state_requests": ProductChangeStateRequestViewSet,
        "pricing-groups": PricingGroupViewSet,
    },
    "branch",
)
branch_service_area_router = register_model_routes(
    router,
    "zones",
    BranchServiceZoneViewSet,
    {"delivery-time-slots": DeliveryTimeSlotViewSet},
    "zone",
)

branch_delivery_time_slot_router = register_model_routes(
    router, "delivery-time-slots", DeliveryTimeSlotViewSet, {}, "delivery_time_slot"
)

urlpatterns = [
    path("products/", include("branches.products.urls", namespace="products")),
    path("users/", include("branches.users.urls", namespace="users")),
]
urlpatterns += router.urls
urlpatterns += branch_router.urls
urlpatterns += branch_service_area_router.urls
# urlpatterns += branch_delivery_time_slot_router.urls
