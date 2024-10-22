from rest_framework import generics, viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from core.base.viewsets import SuperModelViewSet
from core.base.viewsets import FieldsMixin
from users.models import UserAddress
from customers.utils import CustomerUtils
from .serializers import InformationSerializer, AddressSerializer


class Information(FieldsMixin, generics.GenericAPIView):
    serializer_class = InformationSerializer()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user


class AddressViewSet(SuperModelViewSet):
    serializer_class = AddressSerializer()
    queryset = UserAddress.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserAddress.objects.filter(user=self.request.user)

        else:
            anonymous = CustomerUtils.get_anonymous_customer(self.request)
            if anonymous is None:
                return UserAddress.objects.none()

            return UserAddress.objects.filter(anonymous=anonymous)
