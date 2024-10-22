from django.urls import path, include
from users.auth.views import (
    CheckUserNameView,
)

app_name = "auth"

urlpatterns = [
    path('check-username/', CheckUserNameView.as_view(), name='check_username'),
]
