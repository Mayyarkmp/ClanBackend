from django.db.models import Q
from rest_framework import viewsets, status, mixins
from rest_framework.exceptions import NotFound
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from core.base.viewsets import SuperModelViewSet
from branches.products.models import ProductQuantity
from branches.products.serializers import ProductQuantitySerializer
from core.base.filters import ArrayFilter
from django.contrib.postgres.fields import ArrayField
from djmoney.money import Money
from django_filters import FilterSet

from .models import (
    Category,
    Unit,
    ProductPrice,
    PricingGroup,
    Supplier,
    Product,
    ProductUnit,
    Group,
    Brand,
)
from .serializers import (
    CategorySerializer,
    UnitSerializer,
    ProductPriceSerializer,
    PricingGroupSerializer,
    GroupSerializer,
    SupplierSerializer,
    ProductSerializer,
    ProductImportSerializer,
    ProductUnitSerializer,
    SubGroupSerializer,
    MainGroupSerializer,
    ProductPricesSerializer,
    BrandSerializer,
)


class GroupViewSet(SuperModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    parent_lookup_kwargs = {
        "product_pk": "children__products__pk",
        "supplier_pk": "suppliers__pk",
        "group_pk": "parent__pk",
        "pack_pk": ["packs__pk"],
    }

    @action(detail=True, methods=["add"])
    def add(self, request, pk=None):
        group = self.get_object()
        data = request.data
        if data.get("children"):
            children_groups = data.get("children")
            for child_group_id in children_groups:
                child_group = Group.objects.get(pk=child_group_id)
                child_group.parent = group
                child_group.save()
            return Response(
                {"message": "Group updated successfully"}, status=status.HTTP_200_OK
            )
        if data.get("products"):
            products = data.get("products")
            for product_id in products:
                product = Product.objects.get(pk=product_id)
                product.group = group
                product.save()

            return Response(
                {"message": "Group updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Group updated successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="import")
    def import_data(self, request):
        data = request.data
        groups = []
        errors = []

        try:
            with transaction.atomic():
                for index, group_data in enumerate(data):
                    group_errors = []
                    parent_group = None

                    # التعامل مع المجموعة الأم إذا وجدت
                    if group_data.get("parent_id") or group_data.get("parent_name"):
                        parent_defaults = {}
                        if group_data.get("parent_name"):
                            parent_defaults["name"] = group_data.get("parent_name")
                        if group_data.get("parent_id"):
                            parent_group, _ = Group.objects.update_or_create(
                                pk=group_data.get("parent_id"),
                                defaults=parent_defaults,
                            )
                        else:
                            parent_group = Group.objects.create(**parent_defaults)
                    else:
                        parent_group = (
                            None  # يمكن أن يكون None إذا لم يتم تقديم أي معلومات
                        )

                    # إعداد بيانات المجموعة
                    group_defaults = {}
                    if group_data.get("name"):
                        group_defaults["name"] = group_data.get("name")
                    else:
                        group_errors.append("يجب تقديم 'name' للمجموعة.")

                    if group_data.get("profit_margin") is not None:
                        group_defaults["profit_margin"] = group_data.get(
                            "profit_margin"
                        )

                    if parent_group:
                        group_defaults["parent"] = parent_group

                    if group_errors:
                        errors.append(
                            f"أخطاء في المجموعة رقم {index + 1}: "
                            + "؛ ".join(group_errors)
                        )
                        continue

                    if group_data.get("id"):
                        group, _ = Group.objects.update_or_create(
                            pk=group_data.get("id"),
                            defaults=group_defaults,
                        )
                    else:
                        group = Group.objects.create(**group_defaults)

                    groups.append(group)

        except Exception as e:
            return Response(
                {
                    "message": f"خطأ في استيراد المجموعات: {str(e)}",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if errors:
            serializer = GroupSerializer(groups, many=True)
            return Response(
                {
                    "message": "تم استيراد بعض المجموعات مع وجود أخطاء.",
                    "data": serializer.data,
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MainGroupViewSet(SuperModelViewSet):
    queryset = Group.objects.filter(parent__isnull=True)
    serializer_class = MainGroupSerializer
    # filter_fields = ['created_at', 'updated_at', 'profit_margin',]
    parent_lookup_kwargs = {
        "product_pk": ["children__products__pk"],
        "supplier_pk": ["suppliers__pk"],
        "sub_group_pk": ["children__pk"],
        "pack_pk": ["packs__pk"],
    }

    @action(detail=True, methods=["add"])
    def add(self, request, pk=None):
        group = self.get_object()
        data = request.data
        if data.get("children"):
            children_groups = data.get("children")
            for child_group_id in children_groups:
                child_group = Group.objects.get(pk=child_group_id)
                child_group.parent = group
                child_group.save()
            return Response(
                {"message": "Group updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Group updated successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="import")
    def import_data(self, request):
        data = request.data
        main_groups = []
        errors = []

        try:
            with transaction.atomic():
                for index, group_data in enumerate(data):
                    group_errors = []

                    # تأكد من أن المجموعة الرئيسية ليس لها parent
                    group_defaults = {"parent": None}

                    if group_data.get("name"):
                        group_defaults["name"] = group_data.get("name")
                    else:
                        group_errors.append("يجب تقديم 'name' للمجموعة الرئيسية.")

                    if group_data.get("profit_margin") is not None:
                        group_defaults["profit_margin"] = group_data.get(
                            "profit_margin"
                        )

                    if group_errors:
                        errors.append(
                            f"أخطاء في المجموعة الرئيسية رقم {index + 1}: "
                            + "؛ ".join(group_errors)
                        )
                        continue

                    if group_data.get("id"):
                        group, _ = Group.objects.update_or_create(
                            pk=group_data.get("id"),
                            defaults=group_defaults,
                        )
                    else:
                        group = Group.objects.create(**group_defaults)

                    main_groups.append(group)

        except Exception as e:
            return Response(
                {
                    "message": f"خطأ في استيراد المجموعات الرئيسية: {str(e)}",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if errors:
            serializer = MainGroupSerializer(main_groups, many=True)
            return Response(
                {
                    "message": "تم استيراد بعض المجموعات الرئيسية مع وجود أخطاء.",
                    "data": serializer.data,
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        serializer = MainGroupSerializer(main_groups, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubGroupViewSet(SuperModelViewSet):
    queryset = Group.objects.filter(parent__isnull=False)
    serializer_class = SubGroupSerializer
    parent_lookup_kwargs = {
        "product_pk": ["products__pk"],
        "supplier_pk": ["suppliers__pk"],
        "group_pk": ["parent__pk"],
        "main_group_pk": ["parent__pk"],
        "pack_pk": ["packs__pk"],
    }

    @action(detail=True, methods=["add"])
    def add(self, request, pk=None):
        group = self.get_object()
        data = request.data
        if data.get("products"):
            products = data.get("products")
            for product_id in products:
                product = Product.objects.get(pk=product_id)
                product.group = group
                product.save()
            return Response(
                {"message": "Group updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Group updated successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="import")
    def import_data(self, request):
        data = request.data
        sub_groups = []
        errors = []

        try:
            with transaction.atomic():
                for index, group_data in enumerate(data):
                    group_errors = []
                    parent_group = None

                    # التعامل مع المجموعة الأم (يجب أن تكون موجودة)
                    if group_data.get("parent_id") or group_data.get("parent_name"):
                        parent_defaults = {}
                        if group_data.get("parent_name"):
                            parent_defaults["name"] = group_data.get("parent_name")
                        if group_data.get("parent_id"):
                            parent_group, _ = Group.objects.update_or_create(
                                pk=group_data.get("parent_id"),
                                defaults=parent_defaults,
                            )
                        else:
                            parent_group = Group.objects.create(**parent_defaults)
                    else:
                        group_errors.append(
                            "يجب تقديم 'parent_id' أو 'parent_name' للمجموعة الفرعية."
                        )

                    # إعداد بيانات المجموعة الفرعية
                    group_defaults = {}
                    if group_data.get("name"):
                        group_defaults["name"] = group_data.get("name")
                    else:
                        group_errors.append("يجب تقديم 'name' للمجموعة الفرعية.")

                    if group_data.get("profit_margin") is not None:
                        group_defaults["profit_margin"] = group_data.get(
                            "profit_margin"
                        )

                    if parent_group:
                        group_defaults["parent"] = parent_group

                    if group_errors:
                        errors.append(
                            f"أخطاء في المجموعة الفرعية رقم {index + 1}: "
                            + "؛ ".join(group_errors)
                        )
                        continue

                    if group_data.get("id"):
                        group, _ = Group.objects.update_or_create(
                            pk=group_data.get("id"),
                            defaults=group_defaults,
                        )
                    else:
                        group = Group.objects.create(**group_defaults)

                    sub_groups.append(group)

        except Exception as e:
            return Response(
                {
                    "message": f"خطأ في استيراد المجموعات الفرعية: {str(e)}",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if errors:
            serializer = SubGroupSerializer(sub_groups, many=True)
            return Response(
                {
                    "message": "تم استيراد بعض المجموعات الفرعية مع وجود أخطاء.",
                    "data": serializer.data,
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        serializer = SubGroupSerializer(sub_groups, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupplierViewSet(SuperModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    parent_lookup_kwargs = {
        "product_pk": ["products__pk"],
        "category_pk": ["categories__pk"],
        "group_pk": ["groups__pk"],
        "sup_group_pk": ["groups__pk"],
        "main_group_pk": ["groups__pk"],
        "pack_pk": ["packs__pk"],
    }

    @action(detail=True, methods=["add"])
    def add(self, request, pk=None):
        supplier = self.get_object()
        data = request.data
        try:
            if data.get("products"):
                products = data.get("products")
                for product_id in products:
                    product = Product.objects.get(pk=product_id)
                    product.supplier = supplier
                    product.save()

            if data.get("categories"):
                categories = data.get("categories")
                for category_id in categories:
                    category = Category.objects.get(pk=category_id)
                    category.suppliers.add(supplier)

            if data.get("groups"):
                groups = data.get("groups")
                for group_id in groups:
                    group = Group.objects.get(pk=group_id)
                    group.suppliers.add(supplier)

            return Response(
                {"message": "Supplier updated successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "Can not update suppliers", "error": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], url_path="import")
    def import_data(self, request):
        data = request.data
        suppliers = []
        errors = []

        try:
            with transaction.atomic():
                for index, supplier_data in enumerate(data):
                    supplier_errors = []

                    supplier_defaults = {}
                    if supplier_data.get("name"):
                        supplier_defaults["name"] = supplier_data.get("name")
                    else:
                        supplier_errors.append("يجب تقديم 'name' للمورد.")

                    if supplier_data.get("name_en"):
                        supplier_defaults["name_en"] = supplier_data.get("name_en")

                    if supplier_errors:
                        errors.append(
                            f"أخطاء في المورد رقم {index + 1}: "
                            + "؛ ".join(supplier_errors)
                        )
                        continue

                    if supplier_data.get("id"):
                        supplier, _ = Supplier.objects.update_or_create(
                            pk=supplier_data.get("id"),
                            defaults=supplier_defaults,
                        )
                    else:
                        supplier = Supplier.objects.create(**supplier_defaults)

                    suppliers.append(supplier)

        except Exception as e:
            return Response(
                {
                    "message": f"خطأ في استيراد الموردين: {str(e)}",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if errors:
            serializer = SupplierSerializer(suppliers, many=True)
            return Response(
                {
                    "message": "تم استيراد بعض الموردين مع وجود أخطاء.",
                    "data": serializer.data,
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductViewSet(SuperModelViewSet):
    queryset = Product.objects.all().order_by("-updated_at")
    serializer_class = ProductSerializer
    lookup_fields = ["pk", "sq"]
    parent_lookup_kwargs = {
        "main_group_pk": ["group__parent__pk"],
        "sub_group_pk": ["group__pk"],
        "group_pk": ["group__pk"],
        "supplier_pk": ["supplier__pk"],
        "category_pk": ["categories__pk"],
        "unit_pk": ["units__unit__pk"],
        "pricing_group_pk": ["prices__pricing_groups__pk"],
        "barcode_pk": ["barcodes__pk"],
        "pack_pk": ["packs__pk"],
    }

    @action(detail=False, methods=["get"])
    def actions(self, request):
        return Response(
            [
                {
                    "label": "حذف",
                    "method": "DELETE",
                    "endpoint": "/delete",
                }
            ]
        )

    @action(detail=False, methods=["delete"])
    def delete(self, request):
        data = request.data
        ids = data.get("items")

        if ids:
            if isinstance(ids, str) and ids == "*":
                self.queryset.all().delete()
                return Response({"message": "تم حذف جميع المنتجات"})

            elif isinstance(ids, (tuple, list)):
                self.queryset.filter(id__in=ids).delete()

                return Response({"message": "تم حذف المنتجات المحددة بنجاح"})

        return Response({"message": "خدث خطأ غير معروف او انه ليس لديك الصلاحية"})

    @action(detail=False, methods=["post"], url_path="import")
    def create_many(self, request):
        data = request.data
        errors = {}
        products = {}

        try:
            with transaction.atomic():
                for index, product_data in enumerate(data):
                    serializer = ProductImportSerializer(data=product_data)
                    if not serializer.is_valid():
                        errors[product_data.get("index")] = serializer.errors.get(
                            "error"
                        )
                        continue

                    product = serializer.save()
                    products[product_data.get("index")] = ProductSerializer(
                        product
                    ).data

        except Exception as e:
            print(e)
            return Response(
                {
                    "message": "حدث خطأ قي السيرفر أثناء استيراد المنتجات",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(errors.values()) > 0:
            return Response(
                {
                    "message": "هناك اخطاء في بيانات المنتجات يرجى معالجتها.",
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        return Response(
            {
                "message": "تم استيراد المنتجات بنجاح.",
                "items": products,
            },
            status=status.HTTP_201_CREATED,
        )


class ProductUnitFilter(FilterSet):
    class Meta:
        model = ProductUnit
        fields = [
            "barcodes",
            "unit",
            "cost",
            "price",
            "quantity",
        ]  # إضافة الحقول التي تريد تصفيتها
        filter_overrides = {
            ArrayField: {
                "filter_class": ArrayFilter,  # تعيين الفلتر المخصص لـ ArrayField
            },
        }


class ProductUnitViewSet(SuperModelViewSet):
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer
    filterset_class = ProductUnitFilter
    parent_lookup_kwargs = {
        "product_pk": ["product__pk"],
        "main_group_pk": ["product__group__parent__pk"],
        "sub_group_pk": ["product__group__pk"],
        "group_pk": ["product__group__pk"],
        "supplier_pk": ["product__supplier__pk"],
        "category_pk": ["product__categories__pk"],
        "unit_pk": ["units__unit__pk"],
        "pricing_group_pk": ["prices__pricing_groups__pk"],
        "pack_pk": ["product__packs__pk"],
    }


# Category ViewSet
class CategoryViewSet(SuperModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "supplier_pk": "suppliers__pk",
        "category_pk": "parent__pk",
        "pack_pk": ["packs__pk"],
    }

    @action(detail=True, methods=["add"])
    def add(self, request, pk=None):
        category = self.get_object()
        data = request.data
        if data.get("children"):
            children_categories = data.get("children")
            for child_category_id in children_categories:
                child_category = Category.objects.get(pk=child_category_id)
                child_category.parent = category
                child_category.save()
            return Response(
                {"message": "Category updated successfully"}, status=status.HTTP_200_OK
            )

        if data.get("products"):
            products = data.get("products")
            for product_id in products:
                product = Product.objects.get(pk=product_id)
                product.categories.add(category)
                product.save()

        return Response(
            {"message": "Category updated successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="import")
    def import_data(self, request):
        data = request.data
        categories = []
        errors = []

        try:
            with transaction.atomic():
                for index, category_data in enumerate(data):
                    category_errors = []
                    parent_category = None

                    # التعامل مع الفئة الأم إذا وجدت
                    if category_data.get("parent_id") or category_data.get(
                        "parent_name"
                    ):
                        parent_defaults = {}
                        if category_data.get("parent_name"):
                            parent_defaults["name"] = category_data.get("parent_name")
                        if category_data.get("parent_id"):
                            parent_category, _ = Category.objects.update_or_create(
                                pk=category_data.get("parent_id"),
                                defaults=parent_defaults,
                            )
                        else:
                            parent_category = Category.objects.create(**parent_defaults)
                    else:
                        parent_category = (
                            None  # يمكن أن يكون None إذا لم يتم تقديم أي معلومات
                        )

                    # إعداد بيانات الفئة
                    category_defaults = {}
                    if category_data.get("name"):
                        category_defaults["name"] = category_data.get("name")
                    else:
                        category_errors.append("يجب تقديم 'name' للفئة.")

                    if category_data.get("name_en"):
                        category_defaults["name_en"] = category_data.get("name_en")

                    if parent_category:
                        category_defaults["parent"] = parent_category

                    if category_errors:
                        errors.append(
                            f"أخطاء في الفئة رقم {index + 1}: "
                            + "؛ ".join(category_errors)
                        )
                        continue

                    if category_data.get("id"):
                        category, _ = Category.objects.update_or_create(
                            pk=category_data.get("id"),
                            defaults=category_defaults,
                        )
                    else:
                        category = Category.objects.create(**category_defaults)

                    categories.append(category)

        except Exception as e:
            return Response(
                {
                    "message": f"خطأ في استيراد الفئات: {str(e)}",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if errors:
            serializer = CategorySerializer(categories, many=True)
            return Response(
                {
                    "message": "تم استيراد بعض الفئات مع وجود أخطاء.",
                    "data": serializer.data,
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Unit ViewSet
class UnitViewSet(SuperModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    parent_lookup_kwargs = {
        "product_price_pk": ["products_prices__pk"],
        "product_cost_pk": ["products_costs__pk"],
        "pricing_group_pk": [
            "products_prices__pricing_groups__pk",
            "products_costs__pricing_groups__pk",
        ],
        "product_pk": ["products_prices__product__pk", "products_costs__product__pk"],
        "barcode_pk": ["products_barcodes__pk"],
    }

    @action(detail=False, methods=["post"], url_path="import")
    def import_data(self, request):
        data = request.data
        units = []
        errors = []

        try:
            with transaction.atomic():
                for index, unit_data in enumerate(data):
                    unit_errors = []
                    factor_unit = None

                    # التعامل مع وحدة العامل إذا وجدت
                    if unit_data.get("factor_unit_id") or unit_data.get(
                        "factor_unit_name"
                    ):
                        factor_unit_filters = Q()
                        if unit_data.get("factor_unit_id"):
                            factor_unit_filters |= Q(pk=unit_data.get("factor_unit_id"))
                        if unit_data.get("factor_unit_name"):
                            factor_unit_filters |= Q(
                                name=unit_data.get("factor_unit_name")
                            )
                        factor_unit = Unit.objects.filter(factor_unit_filters).first()
                        if not factor_unit:
                            unit_errors.append("وحدة العامل 'factor_unit' غير موجودة.")
                    else:
                        factor_unit = None

                    # إعداد بيانات الوحدة
                    unit_defaults = {}
                    if unit_data.get("name"):
                        unit_defaults["name"] = unit_data.get("name")
                    else:
                        unit_errors.append("يجب تقديم 'name' للوحدة.")

                    if unit_data.get("codename"):
                        unit_defaults["codename"] = unit_data.get("codename")
                    else:
                        unit_errors.append("يجب تقديم 'codename' للوحدة.")

                    if factor_unit:
                        unit_defaults["factor_unit"] = factor_unit

                    if unit_data.get("conversion_factor") is not None:
                        unit_defaults["conversion_factor"] = unit_data.get(
                            "conversion_factor"
                        )

                    if unit_errors:
                        errors.append(
                            f"أخطاء في الوحدة رقم {index + 1}: "
                            + "؛ ".join(unit_errors)
                        )
                        continue

                    if unit_data.get("id"):
                        unit, _ = Unit.objects.update_or_create(
                            pk=unit_data.get("id"),
                            defaults=unit_defaults,
                        )
                    else:
                        unit = Unit.objects.create(**unit_defaults)

                    units.append(unit)

        except Exception as e:
            return Response(
                {
                    "message": f"خطأ في استيراد الوحدات: {str(e)}",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if errors:
            serializer = UnitSerializer(units, many=True)
            return Response(
                {
                    "message": "تم استيراد بعض الوحدات مع وجود أخطاء.",
                    "data": serializer.data,
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ProductPrice ViewSet
class ProductPriceViewSet(SuperModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    parent_lookup_kwargs = {
        "product_pk": ["product__pk"],
        "branch_product_pk": "product__branches__pk",
        "unit_pk": ["unit__pk"],
        "barcode_pk": ["product__barcodes__pk"],
    }


class ProductPricesViewSet(SuperModelViewSet):
    queryset = Product.objects.filter()
    serializer_class = ProductPricesSerializer


# PricingGroup ViewSet
class PricingGroupViewSet(SuperModelViewSet):
    queryset = PricingGroup.objects.all()
    serializer_class = PricingGroupSerializer
    parent_lookup_kwargs = {
        "product_price_pk": ["products_prices__pk"],
        "unit_pk": ["products_prices__unit__pk"],
        "product_pk": ["products_prices__product__pk"],
    }


class ProductQuantityViewSet(SuperModelViewSet):
    queryset = ProductQuantity.objects.all()
    serializer_class = ProductQuantitySerializer
    parent_lookup_kwargs = {
        "unit_pk": ["unit__pk"],
        "product_pk": ["product__product__pk"],
    }


class BrandViewSet(SuperModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    parent_lookup_kwargs = {
        "product_pk": ["products__pk"],
        "pack_pk": ["packs__pk"],
        "sub_pack_pk": ["packs__pk"],
        "main_pack_pk": ["packs__pk"],
    }

    @action(detail=True, methods=["add"])
    def add(self, request, pk=None):
        brand = self.get_object()
        data = request.data
        if data.get("products"):
            products = data.get("products")
            for product_id in products:
                product = Product.objects.get(pk=product_id)
                product.brand = brand
                product.save()
            return Response(
                {"message": "Brand updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Brand updated successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="import")
    def import_data(self, request):
        data = request.data
        brands = []
        errors = []

        try:
            with transaction.atomic():
                for index, brand_data in enumerate(data):
                    brand_errors = []

                    brand_defaults = {}
                    if brand_data.get("name"):
                        brand_defaults["name"] = brand_data.get("name")
                    else:
                        brand_errors.append("يجب تقديم 'name' للعلامة التجارية.")

                    if brand_data.get("name_en"):
                        brand_defaults["name_en"] = brand_data.get("name_en")

                    if brand_errors:
                        errors.append(
                            f"أخطاء في العلامة التجارية رقم {index + 1}: "
                            + "؛ ".join(brand_errors)
                        )
                        continue

                    if brand_data.get("id"):
                        brand, _ = Brand.objects.update_or_create(
                            pk=brand_data.get("id"),
                            defaults=brand_defaults,
                        )
                    else:
                        brand = Brand.objects.create(**brand_defaults)

                    brands.append(brand)

        except Exception as e:
            return Response(
                {
                    "message": f"خطأ في استيراد العلامات التجارية: {str(e)}",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if errors:
            serializer = BrandSerializer(brands, many=True)
            return Response(
                {
                    "message": "تم استيراد بعض العلامات التجارية مع وجود أخطاء.",
                    "data": serializer.data,
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductQuantityViewSet(SuperModelViewSet):
#     queryset = ProductQuantity.objects.all()
#     serializer_class = ProductQuantitySerializer
#     parent_lookup_kwargs = {
#         "product_pk": ["product__pk"],
#         "unit_pk": ["unit__pk"],
#     }

#     def create(self, request, *args, **kwargs):
#         product_id = kwargs.get("product_pk")
#         unit_id = kwargs.get("unit_pk")
#         data = request.data
#         product = Product.objects.get(pk=product_id)
#         unit = Unit.objects.get(pk=unit_id)
#         try:
#             quantity = ProductQuantity.objects.get(
#                 product=product, unit=unit
#             )
#             quantity.quantity = data.get("quantity")
#             quantity.save()
#             serializer = ProductQuantitySerializer(quantity)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except ProductQuantity.DoesNotExist:
#             data["product"] = product_id
#             data["unit"] = unit_id
#             serializer = ProductQuantitySerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save
