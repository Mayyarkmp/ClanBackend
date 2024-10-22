from .models import BranchUser, Delivery, Preparer, Staff, WorkPeriod, Zone
from .models import Manager
from core.base.serializers import SuperModelSerializer
from branches.serializers import BranchSerializer
from rest_framework import serializers


class BranchUserSerializer(SuperModelSerializer):
    class Meta:
        model = BranchUser
        fields = "__all__"


class ManagerSerializer(SuperModelSerializer):
    class Meta:
        model = Manager
        fields = "__all__"


class ManagerBranchMergingSerializer(serializers.Serializer):
    managerSerializer = ManagerSerializer()
    branchSerializer = BranchSerializer()


class DeliverySerializer(SuperModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class PreparerSerializer(SuperModelSerializer):
    class Meta:
        model = Preparer
        fields = "__all__"


class StaffSerializer(SuperModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class WorkPeriodSerializer(SuperModelSerializer):
    class Meta:
        model = WorkPeriod
        fields = "__all__"


class ZoneSerializer(SuperModelSerializer):
    class Meta:
        model = Zone
        fields = "__all__"
