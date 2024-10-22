from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from guardian.shortcuts import get_objects_for_user
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from core.base.viewsets import SuperModelViewSet
from customers.models import Customer
from orders.models import Cart, CartItem, Order
from customers.utils import CustomerUtils
from customers.cart.serializers import (
    CartItemSerializer,
    CartSerializer,
    OrderSerializer,
)
from customers.permissions import BrowsingKeyPermission


class IsCartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.customer is None:
            anonymous = CustomerUtils.get_anonymous_customer(request)
            if anonymous is None:
                return False
            return obj.anonymous == anonymous

        return obj.customer == request.user

class CartViewSet(SuperModelViewSet):
    permission_classes = [IsCartOwner, BrowsingKeyPermission]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        # Get carts for authenticated user or anonymous customer
        if self.request.user.is_authenticated:
            return Cart.objects.filter(customer=self.request.user)
        else:
            anonymous = CustomerUtils.get_anonymous_customer(self.request)
            if anonymous:
                return Cart.objects.filter(anonymous=anonymous)
            return Cart.objects.none()

    def list(self, request):
        browsing_key = CustomerUtils.get_browsing_key(request)
        cart = self.get_queryset().filter(status=Cart.Status.OPEN).first()

        # Determine the customer or anonymous user
        customer = self.request.user if self.request.user.is_authenticated and isinstance(self.request.user, Customer) else None
        anonymous = CustomerUtils.get_anonymous_customer(request)

        # Check if the open cart has the correct browsing key and update if needed
        if cart:
            if cart.browsing_key != browsing_key:
                cart.browsing_key = browsing_key
                cart.delivery_type = browsing_key.delivery_type
                cart.save()

        # If no open cart found, try to find a cart with the same browsing key or create a new one
        if not cart:
            cart = self.get_queryset().filter(browsing_key=browsing_key).first()


        if not cart and anonymous or customer:
            cart = self.get_queryset().create(
                customer=customer,
                anonymous=anonymous,
                browsing_key=browsing_key,
                delivery_type=browsing_key.delivery_type,
            )

        # Serialize and return the cart data
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def items(self, request):
        cart = self.get_queryset().filter(status=Cart.Status.OPEN).first()
        if not cart:
            return Response({"detail": _("No open cart found.")}, status=404)

        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        # Instead of deleting the cart, mark it as canceled
        instance.mark_as_canceled()

    @action(detail=True, methods=['post'])
    def set_open(self, request, pk=None):
        # Mark the selected cart as open
        cart = self.get_object()
        cart.mark_as_open()
        return Response({"status": "cart opened", "cart_id": cart.pk})



class CartItemsViewSet(SuperModelViewSet):
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        # Find the open cart for the customer
        cart = Cart.objects.filter(customer=request.user, status=Cart.Status.OPEN).first()
        if not cart:
            return Response({"detail": _("No open cart found.")}, status=404)

        # Add items to the open cart
        request.data['cart'] = cart.pk
        return super().create(request, *args, **kwargs)
