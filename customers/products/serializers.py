from rest_framework import serializers
from core.base.serializers import SuperSerializer, SuperModelSerializer
from offers.discounts.serializers import OfferSerializer
from customers.utils import CustomerUtils
from products.models import ProductUnit, Product
from .utils import get_price_for_product


class ProductSerializer(SuperSerializer):
    offer = serializers.SerializerMethodField()

    def get_offer(self, obj):
        # استخراج الفرع أو العميل إذا كانت هناك حاجة لهذه البيانات
        request = self.context.get(
            "request"
        )  # الحصول على الطلب للوصول إلى البيانات المتعلقة بالعميل أو الفرع
        browsing_key = CustomerUtils.get_browsing_key(request)
        if not browsing_key:
            return None

        customer = request.user if request and request.user.is_authenticated else None

        # حساب العرض والسعر بناءً على المنتج
        final_price, discount_price, best_offer = get_price_for_product(
            product=obj,
            browsing_key=browsing_key,
            branch=browsing_key.branch,
            customer=customer,
        )

        if best_offer:
            serializer = OfferSerializer(best_offer)

            return {
                "final_price": final_price,
                "discount_price": discount_price,
                "offer": serializer.data if best_offer else None,
            }
        return {}

    class Meta:
        model = Product
        fields = "__all__"


class ProductUnitSerializer(SuperModelSerializer):
    sq = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    name_en = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    description_en = serializers.SerializerMethodField()
    main_group = serializers.SerializerMethodField()
    sub_group = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    packs = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    def get_sq(self, obj):
        return obj.product.sq

    def get_main_group(self, obj):
        return obj.product.group.parent.id if obj.product.group.parent else None

    def get_sub_group(self, obj):
        return obj.product.group.id if obj.product.group else None

    def get_supplier(self, obj):
        return obj.product.supplier.id if obj.product.supplier else None

    def get_categories(self, obj):
        categories = []
        for category in obj.product.categories.all():
            categories.append(category.id)
        return categories

    def get_brand(self, obj):
        return obj.product.brand.id if obj.product.brand else None

    def get_packs(self, obj):
        packs = []
        for pack in obj.product.packs.all():
            packs.append(pack.id)
        return packs

    def get_name(self, obj):
        return obj.product.name

    def get_name_en(self, obj):
        return obj.product.name_en

    def get_description(self, obj):
        return obj.product.description

    def get_description_en(self, obj):
        return obj.product.description_en

    class Meta:
        model = ProductUnit
        exclude = ["cost", "cost_currency"]
