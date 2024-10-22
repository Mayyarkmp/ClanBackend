from core.base import viewsets
from .serializers import (
    PricingGroupSerializer,
    ProductSerializer,
    PrimaryShelfSerializer,
    SubShelfSerializer,
    ShelfSerializer,
    ProductQuantitySerializer,
    ProductPriceSerializer,
    ProductChangeStateRequestSerializer,
    ProductTransferRequestSerializer,
    ProductSupplyRequestSerializer,
    ProductSupplyActionSerializer,
)
from .models import (
    PricingGroup,
    Product,
    PrimaryShelf,
    SubShelf,
    Shelf,
    ProductQuantity,
    ProductPrice,
    ProductChangeStateRequest,
    ProductTransferRequest,
    ProductSupplyRequest,
    ProductSupplyAction,
)


class PricingGroupViewSet(viewsets.SuperModelViewSet):
    queryset = PricingGroup.objects.all()
    serializer_class = PricingGroupSerializer
    parent_lookup_kwargs = {}


class ProductViewSet(viewsets.SuperModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parent_lookup_kwargs = {
        "shelf_pk": {
            "query":"shelves__pk",
            "related_name" : "shelves"
        }
    }


class PrimaryShelfViewSet(viewsets.SuperModelViewSet):
    queryset = PrimaryShelf.objects.all()
    serializer_class = PrimaryShelfSerializer
    parent_lookup_kwargs = {
        "product_pk": "sub_shelves__shelves__products__pk",
        "shelf_pk": "sub_shelves__shelves__pk",
        "sub_shelf_pk": "sub_shelves__pk"
    }


class SubShelfViewSet(viewsets.SuperModelViewSet):
    queryset = SubShelf.objects.all()
    serializer_class = SubShelfSerializer
    parent_lookup_kwargs = {
        "product_pk": "shelves__products__pk",
        "shelf_pk": ["shelves__pk", "primary_shelf__pk"],
        "primary_shelf_pk": "primary_shelf__pk"
    }


class ShelfViewSet(viewsets.SuperModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "primary_shelf_pk": "sub_shelf__primary_shelf__pk",
        "sub_shelf_pk": "sub_shelf__pk"
    }


class ProductQuantityViewSet(viewsets.SuperModelViewSet):
    queryset = ProductQuantity.objects.all()
    serializer_class = ProductQuantitySerializer
    parent_lookup_kwargs = {
        'product_pk': 'product__pk',
        'branch_product_pk': 'product__pk',
        'unit_pk': 'unit__pk',
    }



class ProductPriceViewSet(viewsets.SuperModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    parent_lookup_kwargs = {
        'product_pk': 'product__pk',
        'branch_product_pk': 'product__pk',
        'unit_pk': 'unit__pk',
    }


class ProductChangeStateRequestViewSet(viewsets.SuperModelViewSet):
    queryset = ProductChangeStateRequest.objects.all()
    serializer_class = ProductChangeStateRequestSerializer
    parent_lookup_kwargs = {
        'product_pk': 'product__pk',
        'branch_product_pk': 'product__pk',
        'unit_pk': 'unit__pk',
    }


class ProductTransferRequestViewSet(viewsets.SuperModelViewSet):
    queryset = ProductTransferRequest.objects.all()
    serializer_class = ProductTransferRequestSerializer
    parent_lookup_kwargs = {
        'product_pk': 'product__pk',
    }


class ProductSupplyRequestViewSet(viewsets.SuperModelViewSet):
    queryset = ProductSupplyRequest.objects.all()
    serializer_class = ProductSupplyRequestSerializer
    parent_lookup_kwargs = {
        'product_pk': 'product__pk',
    }


class ProductSupplyActionViewSet(viewsets.SuperModelViewSet):
    queryset = ProductSupplyAction.objects.all()
    serializer_class = ProductSupplyActionSerializer
    parent_lookup_kwargs = {
        'product_pk': 'product__pk',
        'supply_request_pk': 'request__pk',
    }
