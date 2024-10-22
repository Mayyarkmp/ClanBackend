from rest_framework import serializers


class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)


class AppleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
