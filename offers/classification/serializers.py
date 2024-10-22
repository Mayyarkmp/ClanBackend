from .models import Pack, PackGroup, PackSupplier, PackProduct, PackCategory, PackBrand
from core.base.serializers import SuperModelSerializer
from rest_framework.exceptions import ValidationError


class PackSerializer(SuperModelSerializer):
    class Meta:
        model = Pack
        fields = "__all__"

    def validate(self, attrs):
        action = self.context.get("action", None)

        if action == "sub":
            if not attrs.get("parent", None):
                raise ValidationError({"parent": "This field is required."})

        return attrs

    def create(self, validated_data):
        if self.context.get("action") == "sub" and not validated_data.get("parent"):
            raise ValidationError(
                {"parent": "This field is required when creating a sub pack."}
            )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        products = validated_data.pop("products", None)
        groups = validated_data.pop("groups", None)
        categories = validated_data.pop("categories", None)
        brands = validated_data.pop("brands", None)
        suppliers = validated_data.pop("suppliers", None)

        # التعامل مع المنتجات باستخدام الكلاس الوسيط PackProduct
        if products is not None:
            for product in products:
                # نحصل على أو ننشئ العلاقة بين Pack و Product
                pack_product, created = PackProduct.objects.get_or_create(
                    pack=instance, product=product
                )
                # تخصيص الحقول الإضافية في PackProduct
                if not created:
                    pack_product.is_active = (
                        True  # تخصيص الحقول الإضافية إذا كانت موجودة
                    )
                pack_product.save()

        # التعامل مع المجموعات باستخدام الكلاس الوسيط PackGroup
        if groups is not None:
            for group in groups:
                pack_group, created = PackGroup.objects.get_or_create(
                    pack=instance, group=group
                )
                if not created:
                    pack_group.is_active = True
                pack_group.save()

        # التعامل مع الفئات باستخدام الكلاس الوسيط PackCategory
        if categories is not None:
            for category in categories:
                pack_category, created = PackCategory.objects.get_or_create(
                    pack=instance, category=category
                )
                if not created:
                    pack_category.is_active = True
                pack_category.save()

        # التعامل مع الموردين باستخدام الكلاس الوسيط PackSupplier
        if suppliers is not None:
            for supplier in suppliers:
                pack_supplier, created = PackSupplier.objects.get_or_create(
                    pack=instance, supplier=supplier
                )
                if not created:
                    pack_supplier.is_active = True
                pack_supplier.save()

        # التعامل مع العلامات التجارية باستخدام الكلاس الوسيط PackBrand
        if brands is not None:
            for brand in brands:
                pack_brand, created = PackBrand.objects.get_or_create(
                    pack=instance, brand=brand
                )
                if not created:
                    pack_brand.is_active = True
                pack_brand.save()

        # تحديث بقية الحقول
        instance = super().update(instance, validated_data)
        return instance
