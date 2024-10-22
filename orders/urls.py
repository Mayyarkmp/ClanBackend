from core.base.routers import register_model_routes
from rest_framework_nested import routers
from .views import CartViewSet, OrderViewSet, CartItemViewSet

app_name = 'orders'

router = routers.DefaultRouter()
cart_router = register_model_routes(router, 'carts', CartViewSet, {
    'orders': OrderViewSet,
    'items': CartItemViewSet
},"cart")
order_router = register_model_routes(router, '', OrderViewSet, {
    'cart': CartViewSet,
    'items': CartItemViewSet
}, "order")


urlpatterns = [
    
]

urlpatterns += router.urls
urlpatterns += cart_router.urls
urlpatterns += order_router.urls
