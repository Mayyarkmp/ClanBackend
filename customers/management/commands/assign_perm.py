import random
import uuid
from django.utils import timezone
from django.core.management.base import BaseCommand
from products.models import (
    Product,
    Group,
    Category,
    Supplier,
    Brand,
    Unit,
    PricingGroup,
    ProductPrice,
    ProductCost,
)
from guardian.shortcuts import assign_perm, get_anonymous_user


class Command(BaseCommand):
    """Seed Branches, BranchServiceAreas, DeliveryTimeSlots, and GeographicAreas"""

    help = "Seed the database with initial data for Branches, Service Areas, Delivery Time Slots, and Geographic Areas."

    def handle(self, *args, **kwargs):
        user = get_anonymous_user()
        groups = Group.objects.all()
        for group in groups:
            assign_perm("view_group", user, group)

        # تعيين الصلاحيات لجميع التصنيفات
        categories = Category.objects.all()
        for category in categories:
            assign_perm("view_category", user, category)

        # تعيين الصلاحيات لجميع العلامات التجارية
        brands = Brand.objects.all()
        for brand in brands:
            assign_perm("view_brand", user, brand)

        # تعيين الصلاحيات لجميع الوحدات
        units = Unit.objects.all()
        for unit in units:
            assign_perm("view_unit", user, unit)

        # تعيين الصلاحيات لجميع المنتجات
        products = Product.objects.all()
        for product in products:
            assign_perm("view_product", user, product)

        # تعيين الصلاحيات لجميع أسعار المنتجات
        product_prices = ProductPrice.objects.all()
        for product_price in product_prices:
            assign_perm("view_productprice", user, product_price)

        # تعيين الصلاحيات لجميع تكاليف المنتجات
        product_costs = ProductCost.objects.all()
        for product_cost in product_costs:
            assign_perm("view_productcost", user, product_cost)

        # تعيين الصلاحيات لجميع مجموعات التسعير
        pricing_groups = PricingGroup.objects.all()
        for pricing_group in pricing_groups:
            assign_perm("view_pricinggroup", user, pricing_group)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully assigned view permissions to anonymous user!"
            )
        )
