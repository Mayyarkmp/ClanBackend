from django.urls import path, include
from rest_framework import routers
from users.views import SessionView
from .views import GenerateKeyBrowsingView, AnonymousCustomerView, FavoriteViewSet

router = routers.DefaultRouter()
router.register(r"favorites", FavoriteViewSet, basename="products_favorites")

app_name = "customers"

urlpatterns = [
    path("", include("customers.details.urls", namespace="details")),
    path("auth/", include("customers.auth.urls", namespace="auth")),
    path("cart/", include("customers.cart.urls", namespace="carts")),
    path("orders/", include("customers.orders.urls", namespace="orders")),
    path("chat/", include("customers.chat.urls", namespace="chat")),
    path("products/", include("customers.products.urls", namespace="products")),
    path("anonymous/", AnonymousCustomerView.as_view(), name="anonymous"),
    path("session/", SessionView.as_view(), name="session"),
    path("browsing-key/", GenerateKeyBrowsingView.as_view(), name="browsing_key"),
]

urlpatterns += router.urls
