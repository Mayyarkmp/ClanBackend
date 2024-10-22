"""
    Create Fake data for products in branches
"""

import random
import uuid
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.db.utils import IntegrityError
from django_seed import Seed
from djmoney.money import Money

from faker import Faker
from branches.products.models import (
    PricingGroup,
    Product,
    PrimaryShelf,
    SubShelf,
    Shelf,
    ProductQuantity,
    ProductCost,
    ProductPrice,
    ProductChangeStateRequest,
    ProductTransferRequest,
    ProductSupplyRequest,
    ProductSupplyAction,
)
from branches.models import Branch
from branches.users.models import BranchUser, Preparer, Delivery
from core.settings.models import Country, Region, City, SubRegion
from customers.models import Customer
from products.models import Product as GlobalProduct, Unit
from users.models import User, UserAddress
from orders.models import Cart, CartItem, Order
fake = Faker()
fake_local = {"ar": Faker(["ar"]), "en": Faker(["en"])}

LANGUAGES = ["en", "ar"]


class Command(BaseCommand):
    """Seed Branches Products"""

    help = "Seed the database with initial data for Groups, Suppliers, Categories, Products, Units, Pricing Groups, Costs, Prices, and Barcodes."
    p = Point([32, 45])

    def handle(self, *args, **kwargs):
        products = GlobalProduct.objects.all()
        cities = City.objects.all()
        regions = Region.objects.all()
        countries = Country.objects.all()
        sub_regions = SubRegion.objects.all()
        branches = Branch.objects.all()

        # for _ in range(100):
        #     d = Delivery.objects.create(
        #         location=Point(random.random(), random.random()),
        #         phone_number=fake.phone_number(),
        #         email=fake.email(),
        #         username=f"{fake.user_name()}{fake.random_int(min=100, max=999)}",
        #         branch=random.choice(branches),
        #     )
        #     d.set_password("password")
        #     d.save()
        #
        #     p = Preparer.objects.create(
        #         location=Point(random.random(), random.random()),
        #         phone_number=fake.phone_number(),
        #         email=fake.email(),
        #         username=f"{fake.user_name()}{fake.random_int(min=100, max=999)}",
        #         branch=random.choice(branches),
        #     )
        #     p.set_password("password")
        #     p.save()

        preparers = Preparer.objects.all()
        deliveries = Delivery.objects.all()
        # for _ in range(50):
        #     m = Customer.objects.create(
        #         email=fake.email(),
        #         username=f"{fake.user_name()}{fake.random_int(min=100, max=999)}",
        #     )
        #     m.set_password("password")
        #     m.save()
        #     for _ in range(random.randint(1, 5)):
        #         UserAddress.objects.create(
        #             user=m,
        #             street_number=fake.random_int(min=1000, max=999999),
        #             is_default=random.choice([True, False]),
        #             country=random.choice(countries),
        #             region=random.choice(regions),
        #             city=random.choice(cities),
        #             sub_region=random.choice(sub_regions),
        #             location=Point(random.random(), random.random()),
        #
        #         )

        users = Customer.objects.all()
        for _ in range(50):
            customer = random.choice(users)
            if customer.addresses.count() == 0:
                UserAddress.objects.create(
                    user=customer,
                    street_number=fake.random_int(min=1000, max=999999),
                    is_default=random.choice([True, False]),
                    country=random.choice(countries),
                    region=random.choice(regions),
                    city=random.choice(cities),
                    sub_region=random.choice(sub_regions),
                    location=Point(random.random(), random.random()),
                )
            c = Cart.objects.create(
                status=random.choice(Cart.Status.names),
                customer=customer,
                type_of_payment=random.choice(Cart.TypeOfPayment.names),
                delivery_type=random.choice(Cart.Delivery.names),
                user_address=random.choice(customer.addresses.all()),
            )
            for _ in range(random.randint(1, 50)):
                try:
                    product = random.choice(products)
                    unit = random.choice(Unit.objects.filter(products_prices__product=product))
                    quantity = random.randint(1, 10)
                    price = random.choice(product.prices.filter(unit=unit))

                    CartItem.objects.create(
                        product=product,
                        unit=unit,
                        quantity=quantity,
                        price=price.price,
                        cart=c
                    )
                except IndexError:
                    continue
            if c.status == Cart.Status.OPEN or c.status == Cart.Status.CLOSED or c.status == Cart.Status.DELIVERING or c.status == Cart.Status.DELIVERED:
                if c.customer.addresses.count() == 0:
                    for _ in range(random.randint(1, 5)):
                        UserAddress.objects.create(
                            user=c.customer,
                            street_number=fake.random_int(min=1000, max=999999),
                            is_default=random.choice([True, False]),
                            country=random.choice(countries),
                            region=random.choice(regions),
                            city=random.choice(cities),
                            sub_region=random.choice(sub_regions),
                            location=Point(random.random(), random.random()),

                        )
                Order.objects.create(
                    cart=c,
                    status=random.choice(Order.OrderStatus.names),
                    delivery_price=Money(random.randint(5, 50), 'SAR'),
                    total_price=Money(random.randint(100, 500), 'SAR'),
                    ordered_at=timezone.now(),
                    branch=random.choice(branches),
                    preparer=random.choice(preparers),
                    delivery=random.choice(deliveries),
                )

