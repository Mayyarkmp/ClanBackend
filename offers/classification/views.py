from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.base.viewsets import SuperModelViewSet
from .models import Pack
from .serializers import PackSerializer


class PackViewSet(SuperModelViewSet):
    queryset = Pack.objects.all()
    serializer_class = PackSerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "main_group_pk": "groups__parent__pk",
        "sub_group_pk": "groups__pk",
        "group_pk": "groups__pk",
        "category_pk": "categories__pk",
        "supplier_pk": "suppliers__pk",
        "pack_pk": "parent__pk",
    }

    @action(detail=True, methods=["post"])
    def add(self, request, pk=None):
        data = request.data
        products = data.get("products", None)
        groups = data.get("groups", None)
        categories = data.get("categories", None)
        brands = data.get("brands", None)
        suppliers = data.get("suppliers", None)

        pack = self.get_object()

        if products:
            for product in products:
                pack.products.add(product)
        if groups:
            for group in groups:
                pack.groups.add(group)
        if categories:
            for category in categories:
                pack.categories.add(category)
        if brands:
            for brand in brands:
                pack.brands.add(brand)
        if suppliers:
            for supplier in suppliers:
                pack.suppliers.add(supplier)

        pack.save()

        serializer = self.get_serializer(pack)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def remove(self, request, pk=None):
        data = request.data
        products = data.get("products", None)
        groups = data.get("groups", None)
        categories = data.get("categories", None)
        brands = data.get("brands", None)
        suppliers = data.get("suppliers", None)

        pack = self.get_object()

        if products:
            for product in products:
                pack.products.remove(product)
        if groups:
            for group in groups:
                pack.groups.remove(group)
        if categories:
            for category in categories:
                pack.categories.remove(category)
        if brands:
            for brand in brands:
                pack.brands.remove(brand)
        if suppliers:
            for supplier in suppliers:
                pack.suppliers.remove(supplier)

        pack.save()

        serializer = self.get_serializer(pack)
        return Response(serializer.data)


class MainPackViewSet(SuperModelViewSet):
    queryset = Pack.objects.filter(parent__isnull=True)
    serializer_class = PackSerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "main_group_pk": "groups__parent__pk",
        "sub_group_pk": "groups__pk",
        "group_pk": "groups__pk",
        "category_pk": "categories__pk",
        "supplier_pk": "suppliers__pk",
        "pack_pk": "parent__pk",
    }

    @action(detail=True, methods=["post"])
    def add(self, request, pk=None):
        data = request.data
        products = data.get("products", None)
        groups = data.get("groups", None)
        categories = data.get("categories", None)
        brands = data.get("brands", None)
        suppliers = data.get("suppliers", None)

        pack = self.get_object()

        if products:
            for product in products:
                pack.products.add(product)
        if groups:
            for group in groups:
                pack.groups.add(group)
        if categories:
            for category in categories:
                pack.categories.add(category)
        if brands:
            for brand in brands:
                pack.brands.add(brand)
        if suppliers:
            for supplier in suppliers:
                pack.suppliers.add(supplier)

        pack.save()

        serializer = self.get_serializer(pack)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def remove(self, request, pk=None):
        data = request.data
        products = data.get("products", None)
        groups = data.get("groups", None)
        categories = data.get("categories", None)
        brands = data.get("brands", None)
        suppliers = data.get("suppliers", None)

        pack = self.get_object()

        if products:
            for product in products:
                pack.products.remove(product)
        if groups:
            for group in groups:
                pack.groups.remove(group)
        if categories:
            for category in categories:
                pack.categories.remove(category)
        if brands:
            for brand in brands:
                pack.brands.remove(brand)
        if suppliers:
            for supplier in suppliers:
                pack.suppliers.remove(supplier)

        pack.save()

        serializer = self.get_serializer(pack)
        return Response(serializer.data)


class SubPackViewSet(SuperModelViewSet):
    queryset = Pack.objects.filter(parent__isnull=False)
    serializer_class = PackSerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "main_group_pk": "groups__parent__pk",
        "sub_group_pk": "groups__pk",
        "group_pk": "groups__pk",
        "category_pk": "categories__pk",
        "supplier_pk": "suppliers__pk",
        "pack_pk": "parent__pk",
    }

    @action(detail=True, methods=["post"])
    def add(self, request, pk=None):
        data = request.data
        products = data.get("products", None)
        groups = data.get("groups", None)
        categories = data.get("categories", None)
        brands = data.get("brands", None)
        suppliers = data.get("suppliers", None)

        pack = self.get_object()

        if products:
            for product in products:
                pack.products.add(product)
        if groups:
            for group in groups:
                pack.groups.add(group)
        if categories:
            for category in categories:
                pack.categories.add(category)
        if brands:
            for brand in brands:
                pack.brands.add(brand)
        if suppliers:
            for supplier in suppliers:
                pack.suppliers.add(supplier)

        pack.save()

        serializer = self.get_serializer(pack)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def remove(self, request, pk=None):
        data = request.data
        products = data.get("products", None)
        groups = data.get("groups", None)
        categories = data.get("categories", None)
        brands = data.get("brands", None)
        suppliers = data.get("suppliers", None)

        pack = self.get_object()

        if products:
            for product in products:
                pack.products.remove(product)
        if groups:
            for group in groups:
                pack.groups.remove(group)
        if categories:
            for category in categories:
                pack.categories.remove(category)
        if brands:
            for brand in brands:
                pack.brands.remove(brand)
        if suppliers:
            for supplier in suppliers:
                pack.suppliers.remove(supplier)

        pack.save()

        serializer = self.get_serializer(pack)
        return Response(serializer.data)
