from django.urls import path, include
from rest_framework_nested import routers

from branches.views import BranchViewSet
from chat.views import RoomViewSet, MessageViewSet
from permissions.views import PermissionViewSet, GroupViewSet
from .views import CentralUserViewSet, GradeViewSet, WorkPeriodViewSet
from core.base.routers import register_model_routes
app_name = 'users'

router = routers.DefaultRouter()
users_router = register_model_routes(router, "", CentralUserViewSet, {
    "grade": GradeViewSet,
    "branches": BranchViewSet,
    "groups": GroupViewSet,
    "permissions": PermissionViewSet,
    "rooms": RoomViewSet,
    "messages": MessageViewSet,
    "work-periods": WorkPeriodViewSet,
}, "central_user")

grade_router = register_model_routes(router, "grades", GradeViewSet, {
    "users": CentralUserViewSet,
    "work-periods": WorkPeriodViewSet,
})


urlpatterns = [
    path('auth/', include('central.users.auth.urls', namespace='auth'))
]
urlpatterns += router.urls
urlpatterns += users_router.urls