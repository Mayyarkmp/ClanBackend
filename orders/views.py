from  .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from core.base.viewsets import SuperModelViewSet


class CartViewSet(SuperModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    parent_lookup_kwargs = {
        "order_pk": ["cart__orders__pk"],
        "customer_pk": ["customer__pk"],
        'product_pk': ['cart_items__product__pk'],
        'branch_pk': ['branch__pk'],
    }


class CartItemViewSet(SuperModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    parent_lookup_kwargs = {
        "order_pk": ["cart__orders__pk"],
        "cart_pk": ["cart__pk"],
    }


class OrderViewSet(SuperModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    parent_lookup_kwargs = {
        "cart_pk": ["cart__pk"],
        "user_pk": ["user__pk"],
        "branch_pk": ["branch__pk"],
        "delivery_pk": ["delivery__pk"],
        "preparer_pk": ["prepared__pk"],
        "customer_pk": ["customer__pk"],
    }

    def get_queryset(self):
        super().get_queryset()
        delayed = self.request.query_params.get('delayed', None)

        if delayed:
            delayed = delayed.split(',')
            print(delayed)
            return self.queryset.filter(delayed__contains=delayed)

        return self.queryset

