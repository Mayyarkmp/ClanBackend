from rest_framework import serializers
from users.models import User, UserAddress, UserInfo, CardID
from core.base.serializers import SuperModelSerializer


class UserSerializer(SuperModelSerializer):
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_verified_phone_number = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserAddressSerializer(SuperModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get("location"):
            return attrs

        if longitude := attrs.get("longitude"):
            if latitude := attrs.get("latitude"):
                attrs["location"] = f"POINT({longitude} {latitude})"
            else:
                raise serializers.ValidationError("Latitude is required")
        else:
            raise serializers.ValidationError("Longitude is required")

        return attrs


class UserInfoSerializer(SuperModelSerializer):

    class Meta:
        model = UserInfo
        fields = "__all__"


class CardIDSerializer(SuperModelSerializer):

    class Meta:
        model = CardID
        fields = "__all__"
