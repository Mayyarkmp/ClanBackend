from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models.information import UserAddress, UserInfo
from core.base.serializers import SuperModelSerializer
from customers.utils import CustomerUtils


class AddressSerializer(SuperModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"
        read_only_fields = ["id", "uid", "user"]

    def create(self, validated_data):
        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["user"] = user
        else:
            anonymous = CustomerUtils.get_anonymous_customer(self.context["request"])
            if anonymous is not None:
                validated_data["anonymous"] = anonymous

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["user"] = user
        else:
            anonymous = CustomerUtils.get_anonymous_customer(self.context["request"])
            if anonymous is None:
                return ValidationError({"user": "User not found"})
            validated_data["anonymous"] = anonymous

        return super().update(instance, validated_data)


class UserInfoSerializer(SuperModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["user"] = user
        else:
            anonymous = CustomerUtils.get_anonymous_customer(self.context["request"])
            if anonymous is not None:
                validated_data["anonymous"] = anonymous

        return super().create(validated_data)


class InformationSerializer(SuperModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"
