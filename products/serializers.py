import uuid
from django.db.models import Q
from decimal import DivisionByZero, Decimal, ROUND_DOWN
from djmoney.money import Money
from decimal import Decimal
from .models import (
    Group,
    Category,
    Unit,
    Product,
    ProductPrice,
    PricingGroup,
    Supplier,
    Brand,
    ProductUnit,
)
from core.base.serializers import SuperModelSerializer
from rest_framework import serializers

max_integer_digits = 14
decimal_places = 2


class GroupSerializer(SuperModelSerializer):
    sup_groups = serializers.SerializerMethodField()

    def get_sup_groups(self, obj):
        return obj.children.count()

    class Meta:
        model = Group
        fields = "__all__"


class MainGroupSerializer(SuperModelSerializer):
    sup_groups = serializers.SerializerMethodField()

    def get_sup_groups(self, obj):
        return obj.children.count()

    class Meta:
        model = Group
        fields = "__all__"


class SubGroupSerializer(SuperModelSerializer):
    products = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=True
    )
    main_group = serializers.SerializerMethodField()
    # thumbnail = serializers.SerializerMethodField()

    # def get_thumbnail(self, obj):
    #     if obj.images.count() > 0:
    #         return obj.images.objects.get(pk=obj.default_image).file.url

    def get_main_group(self, obj):
        if obj.parent is not None:
            return {
                "name": obj.parent.name,
                "id": obj.parent.id,
            }
        return None

    def get_products(self, obj):
        return obj.products.count()

    class Meta:
        model = Group
        fields = "__all__"


class CategorySerializer(SuperModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        return [ob.id for ob in obj.children.all()]

    class Meta:
        model = Category
        fields = "__all__"


class UnitSerializer(SuperModelSerializer):

    class Meta:
        model = Unit
        fields = "__all__"


class ProductSerializer(SuperModelSerializer):
    number = serializers.CharField(required=False)
    main_group = serializers.SerializerMethodField()
    average_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    cost_currency = serializers.SerializerMethodField()
    price_currency = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    original_price = serializers.SerializerMethodField()
    original_price_currency = serializers.SerializerMethodField()
    barcodes = serializers.SerializerMethodField()
    default_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_default_image(self, obj):
        unit = self.get_product_unit(obj)
        return unit.default_image if unit else None

    def get_images(self, obj):
        unit = self.get_product_unit(obj)
        if unit and unit.images.count() > 0:
            return [
                {"id": image.id, "url": image.file.url} for image in unit.images.all()
            ]

        return None

    def get_barcodes(self, obj):
        unit = self.get_product_unit(obj)
        return unit.barcodes if unit else None

    def get_product_unit(self, obj):
        # التأكد من أن obj.units ليست فارغة قبل محاولة البحث
        if obj.units.exists():
            unit = obj.units.filter(unit__is_factor=True).first() or obj.units.first()
            return unit
        return None

    def get_cost(self, obj):
        unit = self.get_product_unit(obj)
        return unit.cost.amount if unit and unit.cost else None

    def get_unit(self, obj):
        unit = self.get_product_unit(obj)
        return (
            {"id": unit.unit.id, "name": unit.unit.name, "name_en": unit.unit.name_en}
            if unit and unit.unit
            else None
        )

    def get_price(self, obj):
        unit = self.get_product_unit(obj)
        return unit.price.amount if unit and unit.price else None

    def get_original_price(self, obj):
        unit = self.get_product_unit(obj)
        return unit.original_price.amount if unit and unit.original_price else None

    def get_cost_currency(self, obj):
        unit = self.get_product_unit(obj)
        return unit.cost.currency.code if unit and unit.cost else None

    def get_price_currency(self, obj):
        unit = self.get_product_unit(obj)
        return unit.price.currency.code if unit and unit.price else None

    def get_original_price_currency(self, obj):
        unit = self.get_product_unit(obj)
        return (
            unit.original_price.currency.code if unit and unit.original_price else None
        )

    def get_main_group(self, obj):
        # التأكد من وجود group و parent قبل محاولة الوصول إلى الحقول
        if obj.group and obj.group.parent:
            return {
                "name": obj.group.parent.name or "",
                "name_en": obj.group.parent.name_en or "",
                "id": obj.group.parent.id,
            }
        return None

    def get_average_price(self, obj):
        prices = []
        currency = None
        # التأكد من أن obj.units ليست فارغة قبل محاولة البحث
        for product_unit in obj.units.all():
            unit = product_unit.unit
            for price in product_unit.prices.all():
                try:
                    if (
                        unit
                        and unit.conversion_factor is not None
                        and price.price
                        and price.price.amount is not None
                    ):
                        converted_price = (
                            Decimal(unit.conversion_factor) * price.price.amount
                        )
                        prices.append(converted_price)
                        if currency is None:
                            currency = price.price.currency
                except (AttributeError, TypeError, Decimal.InvalidOperation):
                    continue  # تخطي الأخطاء وإكمال الدورة

        try:
            average = sum(prices) / len(prices) if prices else None
        except (DivisionByZero, ZeroDivisionError):
            average = None

        if average is not None and currency is not None:
            return {"amount": round(average, 2), "currency": str(currency)}
        return None

    class Meta:
        model = Product
        fields = "__all__"


class ProductImportSerializer(serializers.Serializer):
    sq = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    main_group_id = serializers.IntegerField(required=False)
    main_group_name = serializers.CharField(required=False)
    group_id = serializers.IntegerField(required=False)
    group_name = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)
    category_name = serializers.CharField(required=False)
    supplier_id = serializers.IntegerField(required=False)
    supplier_name = serializers.CharField(required=False)
    brand_id = serializers.IntegerField(required=False)
    brand_name = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    cost = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    original_price = serializers.DecimalField(
        required=False, max_digits=10, decimal_places=2
    )
    barcodes = serializers.CharField(required=False)

    def parse_money(self, text, max_digits=10, decimal_places=2):
        try:
            # تحويل السعر إلى Decimal
            price = Decimal(text)
        except:
            raise serializers.ValidationError("القيمة المدخلة للسعر غير صحيحة.")

        # قطع الأرقام الزائدة بعد الفاصلة العشرية دون تقريب
        quantize_str = "1." + "0" * decimal_places
        price = price.quantize(Decimal(quantize_str), rounding=ROUND_DOWN)

        # تحويل السعر إلى سلسلة للتحقق من عدد الأرقام
        str_price = format(price, "f")  # لضمان وجود الفاصلة العشرية
        integer_part, _, decimal_part = str_price.partition(".")

        # تحقق من أن عدد الأرقام الإجمالية لا يتجاوز max_digits
        if len(integer_part) + len(decimal_part) > max_digits:
            raise serializers.ValidationError(
                f"تأكد أن القيمة لا تحتوي على أكثر من {max_digits} أرقام في المجموع."
            )

        return price

    def to_internal_value(self, data):
        # معالجة السعر قبل التحقق من الصحة
        if "price" in data:
            data["price"] = self.parse_money(
                data["price"], max_digits=10, decimal_places=2
            )
        if "cost" in data:
            data["cost"] = self.parse_money(
                data["cost"], max_digits=10, decimal_places=2
            )

        return super().to_internal_value(data)

    def validate(self, data):
        warnings = []
        errors = []

        q = Q()
        if data.get("sq"):
            q |= Q(sq=data.get("sq"))
        if data.get("id"):
            q |= Q(id=data.get("id"))

        product = Product.objects.filter(q).first()
        if not product:
            warnings.append("هذا المنتج غير موجود، سيتم إنشاؤه")
            if not data.get("name"):
                errors.append("الاسم مطلوب")

            if data.get("group_id"):
                group = Group.objects.filter(
                    Q(pk=data.get("group_id")) | Q(number=data.get("group_id"))
                ).first()
                if not group:
                    warnings.append(
                        "المجموعة غير موجودة، سيتم إنشاء مجموعة فرعية جديدة"
                    )
                    if not data.get("main_group_id"):
                        errors.append("يرجى إدخال رقم المجموعة الرئيسية")
                    main_group = Group.objects.filter(
                        Q(pk=data.get("main_group_id"))
                        | Q(number=data.get("main_group_id"))
                    ).first()
                    if not main_group:
                        warnings.append("سيتم إنشاء مجموعة رئيسية جديدة")
                        if not data.get("main_group_name"):
                            errors.append("اسم المجموعة الرئيسية مطلوب")
                    if not data.get("group_name"):
                        errors.append("اسم المجموعة الفرعية مطلوب")

        if data.get("price") is not None or data.get("cost") is not None:
            if not data.get("unit"):
                errors.append("يجب تقديم 'الوحدة' إذا تم تقديم 'السعر' أو 'التكلفة'.")
            else:
                warnings.append(
                    "سيتم تحديث التكلفة أو السعر للوحدة " + data.get("unit")
                )

        if data.get("barcodes") and isinstance(data.get("barcodes"), str):
            data["barcodes"] = [data["barcodes"]]

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        data["warnings"] = warnings
        return data

    def create(self, validated_data):
        main_group = None
        if validated_data.get("main_group_id") or validated_data.get("main_group_name"):
            main_group_defaults = {}
            if validated_data.get("main_group_name"):
                main_group_defaults["name"] = validated_data.get("main_group_name")
                main_group_defaults["number"] = validated_data.get("main_group_id")
            main_group, _ = (
                Group.objects.update_or_create(
                    pk=validated_data.get("main_group_id"),
                    defaults={
                        k: v for k, v in main_group_defaults.items() if v is not None
                    },
                )
                if validated_data.get("main_group_id")
                else Group.objects.create(
                    **{k: v for k, v in main_group_defaults.items() if v is not None}
                )
            )

        sub_group = None
        if validated_data.get("group_id") or validated_data.get("group_name"):
            sub_group_defaults = {"parent": main_group} if main_group else {}
            if validated_data.get("group_name"):
                sub_group_defaults["name"] = validated_data.get("group_name")
                sub_group_defaults["number"] = validated_data.get("group_id")
            sub_group, _ = (
                Group.objects.update_or_create(
                    pk=validated_data.get("group_id"),
                    defaults={
                        k: v for k, v in sub_group_defaults.items() if v is not None
                    },
                )
                if validated_data.get("group_id")
                else Group.objects.create(
                    **{k: v for k, v in sub_group_defaults.items() if v is not None}
                )
            )

        category = None
        if validated_data.get("category_id") or validated_data.get("category_name"):
            category_defaults = {}
            if validated_data.get("category_name"):
                category_defaults["name"] = validated_data.get("category_name")
                category_defaults["number"] = validated_data.get("category_id")
            category, _ = (
                Category.objects.update_or_create(
                    pk=validated_data.get("category_id"),
                    defaults={
                        k: v for k, v in category_defaults.items() if v is not None
                    },
                )
                if validated_data.get("category_id")
                else Category.objects.create(
                    **{k: v for k, v in category_defaults.items() if v is not None}
                )
            )

        supplier = None
        if validated_data.get("supplier_id") or validated_data.get("supplier_name"):
            supplier_defaults = {}
            if validated_data.get("supplier_name"):
                supplier_defaults["name"] = validated_data.get("supplier_name")
                supplier_defaults["number"] = validated_data.get("supplier_id")
            supplier, _ = (
                Supplier.objects.update_or_create(
                    pk=validated_data.get("supplier_id"),
                    defaults={
                        k: v for k, v in supplier_defaults.items() if v is not None
                    },
                )
                if validated_data.get("supplier_id")
                else Supplier.objects.create(
                    **{k: v for k, v in supplier_defaults.items() if v is not None}
                )
            )

        brand = None
        if validated_data.get("brand_id") or validated_data.get("brand_name"):
            brand_defaults = {}
            if validated_data.get("brand_name"):
                brand_defaults["name"] = validated_data.get("brand_name")
                brand_defaults["number"] = validated_data.get("brand_id")
            brand, _ = (
                Brand.objects.update_or_create(
                    pk=validated_data.get("brand_id"),
                    defaults={k: v for k, v in brand_defaults.items() if v is not None},
                )
                if validated_data.get("brand_id")
                else Brand.objects.create(
                    **{k: v for k, v in brand_defaults.items() if v is not None}
                )
            )

        sq = validated_data.get("sq")
        product_defaults = {
            "name": validated_data.get("name"),
            "group": sub_group,
            "supplier": supplier,
            "brand": brand,
        }
        product, created = Product.objects.update_or_create(
            sq=sq,
            defaults={k: v for k, v in product_defaults.items() if v is not None},
        )

        if category:
            product.categories.add(category)

        if validated_data.get("unit"):
            unit_filters = (
                Q(name=validated_data.get("unit"))
                | Q(codename=validated_data.get("unit"))
                | Q(codename=str(validated_data.get("unit")).replace(" ", "_"))
            )
            unit = Unit.objects.filter(unit_filters).first() or Unit.objects.create(
                codename=str(validated_data.get("unit")).replace(" ", "_"),
                name=validated_data.get("unit"),
            )

            product_unit_defaults = {
                "price": validated_data.get("price"),
                "number": validated_data.get("id"),
                "price_net": validated_data.get("price_net"),
                "price_gross": validated_data.get("price_gross"),
                "cost": validated_data.get("cost"),
                "original_price": validated_data.get("original_price"),
                "barcodes": validated_data.get("barcodes"),
            }

            product_unit, _ = ProductUnit.objects.update_or_create(
                product=product,
                unit=unit,
                defaults={
                    k: v for k, v in product_unit_defaults.items() if v is not None
                },
            )

        return product

    def update(self, instance, validated_data):
        # تحديث المنتج الحالي
        instance.name = validated_data.get("name", instance.name)
        instance.sq = validated_data.get("sq", instance.sq)
        # تحديث باقي الحقول
        instance.save()

        # التعامل مع الوحدات وبقية العلاقات كما هو موضح في create
        return self.create(validated_data)


class MiniUnitSerializer(SuperModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "name", "name_en", "codename"]


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
        fields = "__all__"


class MiniProductPriceSerializer(SuperModelSerializer):

    class Meta:
        model = ProductPrice
        fields = [
            "id",
            "pricing_group",
            "price",
            "price_currency",
            "original_price",
            "original_price_currency",
        ]


class ProductPricesSerializer(SuperModelSerializer):
    prices = MiniProductPriceSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "uid",
            "name",
            "name_en",
            "group",
            "prices",
            "created_at",
            "updated_at",
        ]


class ProductPriceSerializer(SuperModelSerializer):

    class Meta:
        model = ProductPrice
        fields = "__all__"


class PricingGroupSerializer(SuperModelSerializer):

    class Meta:
        model = PricingGroup
        fields = "__all__"


class SupplierSerializer(SuperModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        if obj.images.count() > 0:
            return obj.images.objects.get(pk=obj.default_image).file.url

    class Meta:
        model = Supplier
        exclude = ["default_image"]


class BrandSerializer(SuperModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
