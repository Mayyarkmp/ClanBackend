from rest_framework import serializers
from .models import Room, Message
from core.base.serializers import SuperModelSerializer


class RoomSerializer(SuperModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"





class MessageSerializer(SuperModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'