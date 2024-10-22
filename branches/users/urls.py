from rest_framework_nested import routers

from core.base.routers import register_model_routes
from orders.views import OrderViewSet
from chat.views import RoomViewSet
from branches.views import BranchViewSet
from branches.products.views import (
    ProductChangeStateRequestViewSet,
    ProductSupplyRequestViewSet,
    ShelfViewSet,
    ProductTransferRequestViewSet,
    PrimaryShelfViewSet,
    SubShelfViewSet,
)
from branches.users.views import (
    BranchUserViewSet,
    ManagerViewSet,
    DeliveryViewSet,
    PreparerViewSet,
    StaffViewSet,
    ZoneViewSet,
    WorkPeriodViewSet,
)

app_name = "users"

router = routers.DefaultRouter()

branch_user_router = register_model_routes(
    router,
    "users",
    BranchUserViewSet,
    {
        "branch": BranchViewSet,
        "orders": OrderViewSet,
        "chat": RoomViewSet,
        "shelves/primary": PrimaryShelfViewSet,
        "shelves/sub": SubShelfViewSet,
        "shelves": ShelfViewSet,
        "supply_requests": ProductSupplyRequestViewSet,
        "transfer_requests": ProductTransferRequestViewSet,
        "change_state_requests": ProductChangeStateRequestViewSet,
        "zones": ZoneViewSet,
        "work_periods": WorkPeriodViewSet,
    },
    "user",
)

manager_router = register_model_routes(
    router,
    "managers",
    ManagerViewSet,
    {
        "branches": BranchViewSet,
        "chat": RoomViewSet,
    },
    "manager",
)

delivery_router = register_model_routes(
    router,
    "deliveries",
    DeliveryViewSet,
    {
        "branch": BranchViewSet,
        "orders": OrderViewSet,
        "chat": RoomViewSet,
        "zones": ZoneViewSet,
        "work_periods": WorkPeriodViewSet,
    },
    "delivery",
)

preparer_router = register_model_routes(
    router,
    "preparers",
    PreparerViewSet,
    {
        "branch": BranchViewSet,
        "orders": OrderViewSet,
        "chat": RoomViewSet,
        "shelves/primary": PrimaryShelfViewSet,
        "shelves/sub": SubShelfViewSet,
        "shelves": ShelfViewSet,
        "supply_requests": ProductSupplyRequestViewSet,
        "transfer_requests": ProductTransferRequestViewSet,
        "change_state_requests": ProductChangeStateRequestViewSet,
        "zones": ZoneViewSet,
        "work_periods": WorkPeriodViewSet,
    },
    "preparer",
)

staff_router = register_model_routes(
    router,
    "staffs",
    StaffViewSet,
    {
        "branch": BranchViewSet,
        "orders": OrderViewSet,
        "chat": RoomViewSet,
        "shelves": ShelfViewSet,
        "supply_requests": ProductSupplyRequestViewSet,
        "transfer_requests": ProductTransferRequestViewSet,
        "change_state_requests": ProductChangeStateRequestViewSet,
        "zones": ZoneViewSet,
        "work_periods": WorkPeriodViewSet,
    },
    "staff",
)


urlpatterns = []

urlpatterns += router.urls
urlpatterns += branch_user_router.urls
urlpatterns += manager_router.urls
urlpatterns += delivery_router.urls
urlpatterns += preparer_router.urls
urlpatterns += staff_router.urls
