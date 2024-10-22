from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "clan"

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("customers/", include("customers.urls", namespace="customers")),
    path("central/", include("central.urls", namespace="central")),
    path("branches/", include("branches.urls", namespace="branches")),
    path("store/", include("products.urls", namespace="products")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("users/", include("users.urls", namespace="users")),
    path("autherization/", include("permissions.urls", namespace="permissions")),
    path("chat/", include("chat.urls", namespace="chat")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
