from rest_framework import serializers
from djmoney.serializers import MoneyField
from core.base.serializers import SuperModelSerializer
from .models import Cart, CartItem, Order


class OrderSerializer(SuperModelSerializer):
    ordered_at = serializers.DateTimeField(read_only=True)
    total_price = MoneyField(null=True)

    class Meta:
        model = Order
        fields = "__all__"


class CartSerializer(SuperModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartItemSerializer(SuperModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
