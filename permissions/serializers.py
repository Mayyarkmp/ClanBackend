from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from guardian.models import GroupObjectPermission, UserObjectPermission





class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'






