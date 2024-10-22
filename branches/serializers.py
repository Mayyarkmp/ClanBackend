from rest_framework import serializers
from core.base.serializers import SuperModelSerializer
from branches.models import Branch, BranchServiceZone, DeliveryTimeSlot


class BranchSerializer(SuperModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Branch
        fields = "__all__"


class BranchServiceZoneSerializer(SuperModelSerializer):

    class Meta:
        model = BranchServiceZone
        fields = "__all__"


class DeliveryTimeSlotSerializer(SuperModelSerializer):

    class Meta:
        model = DeliveryTimeSlot
        fields = "__all__"
