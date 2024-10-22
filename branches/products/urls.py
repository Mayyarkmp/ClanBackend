from rest_framework_nested import routers
from core.base.routers import register_model_routes
from products.views import UnitViewSet,  ProductPriceViewSet as GlobalProductPriceViewSet
from .views import (
    PricingGroupViewSet,
    ProductViewSet,
    PrimaryShelfViewSet,
    SubShelfViewSet,
    ShelfViewSet,
    ProductQuantityViewSet,
    ProductPriceViewSet,
    ProductChangeStateRequestViewSet,
    ProductTransferRequestViewSet,
    ProductSupplyRequestViewSet,
    ProductSupplyActionViewSet,
)
from ..users.views import BranchUserViewSet

app_name = "products"

router = routers.DefaultRouter()


pricing_group_router = register_model_routes(
    router,
    "pricing-groups",
    PricingGroupViewSet,
    {"products": ProductViewSet},
    "pricing_group",
)

primary_shelf_router = register_model_routes(
    router,
    "shelves/primary",
    PrimaryShelfViewSet,
    {
        "sub-shelves": SubShelfViewSet,
        "shelves": ShelfViewSet,
        "products": ProductViewSet,
    },
    "primary_shelf",
)

sub_shelf_router = register_model_routes(
    router,
    "shelves/sub-shelves",
    SubShelfViewSet,
    {
        "shelves": ShelfViewSet,
        "primary": PrimaryShelfViewSet,
        "products": ProductViewSet,
    },
    "sub_shelf",
)

shelf_router = register_model_routes(
    router,
    "shelves",
    ShelfViewSet,
    {
        "primary": PrimaryShelfViewSet,
        "sub-shelf": SubShelfViewSet,
        "products": (ProductViewSet, {
            "branch-prices": ProductPriceViewSet,
            "quantities": ProductQuantityViewSet,
            "prices": GlobalProductPriceViewSet,
        }, "branch_product"),
    },
    "shelf",
)

product_quantity_router = register_model_routes(
    router,
    "product-quantity",
    ProductQuantityViewSet,
    {
        "product": ProductViewSet,
    },
    "product_quantity",
)


product_price_router = register_model_routes(
    router,
    "products-prices",
    ProductPriceViewSet,
    {
        "products": ProductViewSet,
        "unit": UnitViewSet,
        "pricing-group": PricingGroupViewSet,
    },
    "product_price",
)

change_state_request_router = register_model_routes(
    router,
    "change-state-requests",
    ProductChangeStateRequestViewSet,
    {"product": ProductViewSet, "creator": BranchUserViewSet},
    "change_state_request",
)

transfer_request_router = register_model_routes(
    router,
    "transfer-requests",
    ProductTransferRequestViewSet,
    {
        "product": ProductViewSet,
    },
    "transfer_request",
)

supply_request_router = register_model_routes(
    router,
    "supply-requests",
    ProductSupplyRequestViewSet,
    {
        "product": ProductViewSet,
    },
    "supply_request",
)

supply_action_router = register_model_routes(
    router,
    "supply-actions",
    ProductSupplyActionViewSet,
    {
        "product": ProductViewSet,
        "actor": BranchUserViewSet,
    },
    "supply_action",
)

product_router = register_model_routes(
    router,
    "products",
    ProductViewSet,
    {
        "prices": ProductPriceViewSet,
        "change-state-requests": ProductChangeStateRequestViewSet,
        "supply-requests": ProductSupplyRequestViewSet,
        "quantities": ProductQuantityViewSet,
    },
    "product",
)

urlpatterns = []
urlpatterns += router.urls
urlpatterns += pricing_group_router.urls
urlpatterns += primary_shelf_router.urls
urlpatterns += sub_shelf_router.urls
urlpatterns += shelf_router.urls
urlpatterns += product_quantity_router.urls
urlpatterns += product_price_router.urls
urlpatterns += change_state_request_router.urls
urlpatterns += transfer_request_router.urls
urlpatterns += supply_request_router.urls
urlpatterns += supply_action_router.urls
urlpatterns += product_router.urls
