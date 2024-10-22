from django.urls import path
from .views import AddressViewSet, Information
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'addresses', AddressViewSet)

app_name = 'details'

urlpatterns = [
    path('info/', Information.as_view())
] + router.urls