from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from core.base.serializers import SuperModelSerializer
from customers.utils import CustomerUtils
from orders.models import Cart, CartItem


class CartItemSerializer(SuperModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        extra_kwargs = {"cart": {"read_only": True}}  # Make cart field read-only

    def validate(self, attrs):
        cart_pk = self.context["request"].parser_context["kwargs"].get("cart_pk")

        if cart_pk is None:
            raise ValidationError({"cart": "Cart ID is required."})

        try:
            cart = Cart.objects.get(pk=cart_pk)
        except Cart.DoesNotExist:
            raise ValidationError(_(f"Cart with ID {cart_pk} does not exist."))

        # Attach the cart to the validated data
        attrs["cart"] = cart

        return super().validate(attrs)


class CartSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=255, read_only=True)
    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Cart
        fields = ["id", "uid", "delivery_type", "items", "browsing_key", "address"]

    def create(self, validated_data):
        # الوصول إلى request من خلال context
        request = self.context["request"]
        user = request.user
        browsing_key = CustomerUtils.get_browsing_key(request)
        session = CustomerUtils.get_session(request)

        if browsing_key is None:
            raise ValidationError({"browsing_key": _("Browsing key not found")})

        if session is None:
            raise ValidationError({"session": _("Session not found")})

        if user.is_anonymous:
            anonymous = CustomerUtils.get_anonymous_customer(request)
            if anonymous is None:
                raise ValidationError({"anonymous": _("This Device not found")})

            cart = Cart.objects.create(
                anonymous=anonymous,
                browsing_key=browsing_key,
                session=session,
            )
        else:
            cart = Cart.objects.create(
                customer=user,
                browsing_key=browsing_key,
                session=session,
            )

        # استخدام نفس serializer لإرجاع البيانات
        return cart


class OrderSerializer(SuperModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "uid", "status", "delivery_type"]
