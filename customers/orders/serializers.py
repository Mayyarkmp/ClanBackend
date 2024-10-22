from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.base.serializers import SuperSerializer, SuperModelSerializer
from customers.models import BrowsingKey
from customers.utils import CustomerUtils
from users.models import UserAddress
from orders.models import Order, Cart, CartItem
from branches.models import Branch


class CheckDeliverySerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def validate(self, data):
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not (-90 <= latitude <= 90):
            raise ValidationError({"latitude": "Latitude must be between -90 and 90."})
        if not (-180 <= longitude <= 180):
            raise ValidationError(
                {"longitude": "Longitude must be between -180 and 180."}
            )

        return data

    def create_point(self):
        latitude = self.validated_data["latitude"]
        longitude = self.validated_data["longitude"]
        return Point(float(longitude), float(latitude), srid=4326)
