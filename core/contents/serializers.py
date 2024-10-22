from rest_framework import serializers
from core.base.serializers import SuperModelSerializer
from .models import DeliveryTypeContents


class DeliveryTypeContentsSerializer(SuperModelSerializer):
    is_default = serializers.BooleanField(write_only=True, required=False)
    is_draft = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = DeliveryTypeContents
        fields = "__all__"
