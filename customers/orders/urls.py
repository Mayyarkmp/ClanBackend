from django.urls import path
from rest_framework_nested import routers
from .views import (
    CheckDeliveryView,
)
from core.base.routers import register_model_routes

router = routers.DefaultRouter()


app_name = "orders"

urlpatterns = [
    path("delivery/check/", CheckDeliveryView.as_view(), name="check_delivery"),
]
urlpatterns += router.urls
