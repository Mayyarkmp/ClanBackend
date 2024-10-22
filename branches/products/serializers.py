from core.base.serializers import SuperModelSerializer
from rest_framework import serializers
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


class PricingGroupSerializer(SuperModelSerializer):

    class Meta:
        model = PricingGroup
        fields = "__all__"


class ProductSerializer(SuperModelSerializer):
    #

    class Meta:
        model = Product
        fields = "__all__"


class MiniProductSerializer(SuperModelSerializer):
    global_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    name_en = serializers.SerializerMethodField()

    def get_global_id(self, obj):
        return obj.product.id

    def get_name(self, obj):
        return obj.product.name

    def get_name_en(self, obj):
        return obj.product.name_en

    class Meta:
        model = Product
        fields = ["id", "global_id", "name", "name_en", "branch"]


class PrimaryShelfSerializer(SuperModelSerializer):

    class Meta:
        model = PrimaryShelf
        fields = "__all__"


class SubShelfSerializer(SuperModelSerializer):
    class Meta:
        model = SubShelf
        fields = "__all__"


class ShelfSerializer(SuperModelSerializer):
    products = MiniProductSerializer(
        many=True, read_only=True
    )  # لعرض المنتجات عند الجلب
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        write_only=True,
        source="products",
    )

    class Meta:
        model = Shelf
        fields = "__all__"

    def update(self, instance, validated_data):
        products = validated_data.pop("products", None)
        if products is not None:
            instance.products.add(*products)
        instance = super().update(instance, validated_data)
        return instance


class ProductQuantitySerializer(SuperModelSerializer):
    branch = serializers.SerializerMethodField()

    def get_branch(self, obj):
        return obj.product.branch

    class Meta:
        model = ProductQuantity
        fields = "__all__"




class ProductPriceSerializer(SuperModelSerializer):
    class Meta:
        model = ProductPrice
        fields = "__all__"


class ProductChangeStateRequestSerializer(SuperModelSerializer):
    class Meta:
        model = ProductChangeStateRequest
        fields = "__all__"


class ProductTransferRequestSerializer(SuperModelSerializer):
    product = MiniProductSerializer()

    class Meta:
        model = ProductTransferRequest
        fields = "__all__"


class ProductSupplyRequestSerializer(SuperModelSerializer):
    product = MiniProductSerializer()

    class Meta:
        model = ProductSupplyRequest
        fields = "__all__"


class ProductSupplyActionSerializer(SuperModelSerializer):
    class Meta:
        model = ProductSupplyAction
        fields = "__all__"
