from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.base.serializers import SuperModelSerializer
from customers.models import BrowsingKey, AnonymousCustomer
from customers.utils import CustomerUtils
from users.models import UserAddress
from branches.models import Branch


class AnonymousCustomerSerializer(SuperModelSerializer):
    class Meta:
        model = AnonymousCustomer
        fields = ["fingerprint"]


class BrowsingKeySerializer(SuperModelSerializer):
    key = serializers.CharField(
        max_length=255,
        read_only=True,
    )
    address = serializers.PrimaryKeyRelatedField(
        queryset=UserAddress.objects.all(), required=False
    )
    delivery_type = serializers.CharField(max_length=255, required=True)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    branch = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), required=False, write_only=True
    )

    class Meta:
        model = BrowsingKey
        fields = "__all__"

    def validate(self, attrs):
        if (
            hasattr(attrs, "address")
            and hasattr(attrs, "latitude")
            and hasattr(attrs, "longitude")
        ):
            raise ValidationError("You can't provide both address and coordinates.")

        # if (
        #     not hasattr(attrs, "address")
        #     and not hasattr(attrs, "latitude")
        #     and not hasattr(attrs, "longitude")
        # ):
        #     raise ValidationError("You must provide either address or coordinates.")

        if hasattr(attrs, "latitude") and hasattr(attrs, "longitude"):
            latitude = attrs.get("latitude")
            longitude = attrs.get("longitude")

            if not (-90 <= latitude <= 90):
                raise ValidationError(
                    {"latitude": "Latitude must be between -90 and 90."}
                )
            if not (-180 <= longitude <= 180):
                raise ValidationError(
                    {"longitude": "Longitude must be between -180 and 180."}
                )

            attrs["branch"] = CustomerUtils.get_nearest_branch(latitude, longitude)

            address = UserAddress.objects.create(
                user=(
                    self.context.get("request").user
                    if self.context.get("request").user.is_authenticated
                    else None
                ),
                location=CustomerUtils.create_point(latitude, longitude),
                country=CustomerUtils.get_country(attrs.get("branch")),
                region=CustomerUtils.get_region(attrs.get("branch")),
                city=CustomerUtils.get_city(attrs.get("branch")),
            )

        if (
            hasattr(attrs, "address")
            and not hasattr(attrs, "latitude")
            and not hasattr(attrs, "longitude")
        ):
            address = attrs.get("address")

            if not address.is_valid:
                raise ValidationError({"address": "Invalid address."})

            attrs["branch"] = CustomerUtils.get_nearest_branch(
                address.location.y, address.location.x
            )

        return super().validate(attrs)
