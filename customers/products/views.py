from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from core.base import viewsets
from products.models import Group, Product, Brand, Category, ProductUnit
from products.serializers import (
    MainGroupSerializer,
    SubGroupSerializer,
    CategorySerializer,
    BrandSerializer,
    GroupSerializer,
)
from customers.permissions import BrowsingKeyPermission
from customers.utils import CustomerUtils
from offers.classification.serializers import PackSerializer
from offers.classification.models import Pack
from .serializers import ProductSerializer, ProductUnitSerializer


class GroupViewSet(viewsets.SuperReadOnlyModelViewSet):
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Group.objects.filter()
    serializer_class = GroupSerializer
    parent_lookup_kwargs = {
        "product_pk": "children__products__pk",
        "sub_group_pk": "children__pk",
        "category_pk": "products__categories__pk",
        "sub_category_pk": "products__categories__children__pk",
        "brand_pk": "products__brands__pk",
        "pack_pk": "packs__pk",
    }


class MainGroupViewSet(viewsets.SuperReadOnlyModelViewSet):
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Group.objects.filter(parent__isnull=True)
    serializer_class = MainGroupSerializer
    parent_lookup_kwargs = {
        "product_pk": "children__products__pk",
        "sub_group_pk": "children__pk",
        "category_pk": "products__categories__pk",
        "sub_category_pk": "products__categories__children__pk",
        "brand_pk": "products__brands__pk",
        "pack_pk": "packs__pk",
    }


class SubGroupViewSet(viewsets.SuperReadOnlyModelViewSet):
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Group.objects.filter(parent__isnull=False)
    serializer_class = SubGroupSerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "main_group_pk": "parent__pk",
        "category_pk": "products__categories__pk",
        "sub_category_pk": "products__categories__children__pk",
        "brand_pk": "products__brands__pk",
        "pack_pk": "products__packs__pk",
    }


class ProductViewSet(viewsets.SuperReadOnlyModelViewSet):
    permission_classes = [
        BrowsingKeyPermission,
    ]
    serializer_class = ProductUnitSerializer
    queryset = ProductUnit.objects.all()
    parent_lookup_kwargs = {
        "main_group_pk": "product__group__parent__pk",
        "sub_group_pk": "product__group__pk",
        "category_pk": "product__categories__pk",
        "sub_category_pk": "product__categories__children__pk",
        "brand_pk": "product__brand__pk",
        "pack_pk": "product__packs__pk",
    }

    def get_queryset(self):
        browsing_key = CustomerUtils.get_browsing_key(self.request)

        return (
            super().get_queryset()
            # .filter(
            #     branches__branch=browsing_key.branch,
            #     branches__quantities__quantity__gt=0,
            # )
        )


class CategoryViewSet(viewsets.SuperReadOnlyModelViewSet):
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "category_pk": "parent__pk",
        "sub_category_pk": "children__pk",
        "brand_pk": "products__brands__pk",
        "pack_pk": "packs__pk",
        "main_group_pk": "products__groups__parent__pk",
        "sub_group_pk": "products__groups__pk",
    }


class BrandViewSet(viewsets.SuperReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "category_pk": "products__categories__pk",
        "sub_category_pk": "products__categories__children__pk",
        "main_group_pk": "products__groups__parent__pk",
        "sub_group_pk": "products__groups__pk",
    }


class PackViewSet(viewsets.SuperReadOnlyModelViewSet):
    queryset = Pack.objects.all()
    serializer_class = PackSerializer
    parent_lookup_kwargs = {
        "product_pk": "products__pk",
        "category_pk": "categories__pk",
        "sub_category_pk": "categories__children__pk",
        "brand_pk": "brands__pk",
        "main_group_pk": "groups__parent__pk",
        "sub_group_pk": "groups__pk",
    }
