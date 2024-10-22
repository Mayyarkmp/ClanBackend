from django.contrib.auth.models import Group
from django.forms import EmailField
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import CentralUser, AssignedBranches, Grade, WorkPeriod
from core.base.serializers import SuperModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField

# centralCtype = ContentType.objects.get_for_model(CentralUser)


class CentralUserSerializer(SuperModelSerializer):
    phone_number = PhoneNumberField(required=True)
    email = EmailField(required=True)
    # groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.filter(user_type=centralCtype),)

    class Meta:
        model = CentralUser
        # fields = '__all__'
        exclude = ["password", "user_permissions"]


class AssignedBranchesSerializer(SuperModelSerializer):
    class Meta:
        model = AssignedBranches
        fields = "__all__"


class GradeSerializer(SuperModelSerializer):

    class Meta:
        model = Grade
        fields = "__all__"


class WorkPeriodSerializer(SuperModelSerializer):
    class Meta:
        model = WorkPeriod
        fields = "__all__"
