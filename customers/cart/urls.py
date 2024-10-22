from django.urls import include, path
from rest_framework_nested import routers
from .views import CartViewSet, CartItemsViewSet
from core.base.routers import register_model_routes

app_name = "carts"


router = routers.DefaultRouter()


router.register(r'', CartViewSet, basename='cart')



urlpatterns = []

urlpatterns += router.urls
# urlpatterns += cart_router.urls
