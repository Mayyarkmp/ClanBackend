import random
import uuid
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
from core.media.models import Media  # تأكد من تعديل المسار حسب الحاجة
from products.models import (
    Group,
    Supplier,
    Category,
    Product,
    Unit,
    PricingGroup,
    ProductUnit,
    ProductPrice,
    Brand,
)

fake = Faker()
fake_local = {"ar": Faker(["ar"]), "en": Faker(["en"])}


class Command(BaseCommand):
    help = "Seed the database with initial data for Groups, Suppliers, Categories, Products, Units, Pricing Groups, Costs, Prices."

    def handle(self, *args, **kwargs):
        self.seed_groups()
        self.stdout.write(self.style.SUCCESS("Successfully seeded groups!"))
        self.seed_sub_groups()
        self.stdout.write(self.style.SUCCESS("Successfully seeded sub_groups!"))
        self.seed_suppliers()
        self.stdout.write(self.style.SUCCESS("Successfully seeded suppliers!"))
        self.seed_categories()
        self.stdout.write(self.style.SUCCESS("Successfully seeded categories!"))
        self.seed_brands()
        self.stdout.write(self.style.SUCCESS("Successfully seeded brands!"))
        self.seed_units()
        self.stdout.write(self.style.SUCCESS("Successfully seeded units!"))
        self.seed_products()
        self.stdout.write(self.style.SUCCESS("Successfully seeded products!"))
        self.seed_product_units()
        self.stdout.write(self.style.SUCCESS("Successfully seeded product units!"))
        self.seed_pricing_groups()
        self.stdout.write(self.style.SUCCESS("Successfully seeded pricing_groups!"))
        self.seed_product_prices()
        self.stdout.write(self.style.SUCCESS("Successfully seeded product prices!"))
        self.stdout.write(self.style.SUCCESS("Successfully seeded the database!"))

    def seed_groups(self):
        for _ in range(50):
            try:
                Group.objects.create(
                    name=fake_local["ar"].company(),
                    name_en=fake_local["en"].company(),
                    parent=None,
                    number=random.randint(10000, 999999),
                )
            except IntegrityError:
                continue

    def seed_sub_groups(self):
        for _ in range(50):
            try:
                Group.objects.create(
                    name=fake_local["ar"].company(),
                    name_en=fake_local["en"].company(),
                    parent=random.choice(Group.objects.filter(parent__isnull=True)),
                    number=random.randint(10000, 999999),
                )
            except IntegrityError:
                continue

    def seed_suppliers(self):
        for _ in range(50):
            try:
                Supplier.objects.create(
                    name=fake_local["ar"].company(),
                    name_en=fake_local["en"].company(),
                    number=random.randint(10000, 999999),
                )
            except IntegrityError:
                continue

    def seed_categories(self):
        for _ in range(50):
            try:
                Category.objects.create(
                    name=fake_local["ar"].name(),
                    name_en=fake_local["en"].name(),
                    number=random.randint(10000, 999999),
                )
            except IntegrityError:
                continue

    def seed_brands(self):
        for _ in range(50):
            try:
                Brand.objects.create(
                    name=fake_local["ar"].name(),
                    name_en=fake_local["en"].name(),
                    number=random.randint(10000, 999999),
                )
            except IntegrityError:
                continue

    def seed_units(self):
        base_units = [
            {
                "name": "حبة",
                "name_en": "Unit",
                "codename": "unit",
                "is_factor": True,
                "conversion_factor": 1,
            },
            {
                "name": "غرام",
                "name_en": "Gram",
                "codename": "gram",
                "is_factor": True,
                "conversion_factor": 1,
            },
            {
                "name": "علبة",
                "name_en": "Box",
                "codename": "box",
                "is_factor": False,
                "conversion_factor": 12,
                "factor_unit": "unit",
            },
        ]

        for unit in base_units:
            try:
                Unit.objects.get_or_create(
                    codename=unit["codename"],
                    number=random.randint(10000, 999999),
                    is_factor=unit["is_factor"],
                    conversion_factor=unit["conversion_factor"],
                    name=unit["name"],
                    name_en=unit["name_en"],
                    factor_unit=(
                        Unit.objects.get(codename=unit["factor_unit"])
                        if "factor_unit" in unit
                        else None
                    ),
                )
            except IntegrityError:
                continue

        sub_units = [
            {
                "name": "كرتونة",
                "name_en": "Carton",
                "codename": "carton",
                "is_factor": False,
                "conversion_factor": 24,  # 1 كرتونة = 24 علبة
                "factor_unit": "box",
            },
            {
                "name": "كيلوغرام",
                "name_en": "Kilogram",
                "codename": "kilogram",
                "is_factor": False,
                "conversion_factor": 1000,  # 1 كيلوغرام = 1000 غرام
                "factor_unit": "gram",
            },
            {
                "name": "طن",
                "name_en": "Ton",
                "codename": "ton",
                "is_factor": False,
                "conversion_factor": 1000,  # 1 طن = 1000 كيلوغرام
                "factor_unit": "kilogram",
            },
        ]

        for unit in sub_units:
            try:
                Unit.objects.get_or_create(
                    codename=unit["codename"],
                    is_factor=unit["is_factor"],
                    conversion_factor=unit["conversion_factor"],
                    factor_unit=(
                        Unit.objects.get(codename=unit["factor_unit"])
                        if "factor_unit" in unit
                        else None
                    ),
                    name=unit["name"],
                    number=random.randint(10000, 999999),
                    name_en=unit["name_en"],
                )
            except IntegrityError:
                continue

    def seed_pricing_groups(self):
        for _ in range(50):
            try:
                PricingGroup.objects.create(
                    codename=f"{fake.slug()}{fake.random_number(2, True)}",
                    name=fake_local["ar"].word(),
                    name_en=fake_local["en"].word(),
                    number=random.randint(10000, 999999),
                )
            except IntegrityError:
                continue

    def seed_products(self):
        groups = Group.objects.filter(parent__isnull=False)
        suppliers = Supplier.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()

        for _ in range(100):
            try:
                product = Product.objects.create(
                    sq=fake.word(),
                    serial_number=fake.unique.uuid4(),
                    group=random.choice(groups),
                    brand=random.choice(brands),
                    supplier=random.choice(suppliers),
                    type=random.choice(
                        [
                            Product.Types.PRIMARY,
                            Product.Types.SECONDARY,
                            Product.Types.NONE,
                        ]
                    ),
                    name=fake_local["ar"].word(),
                    name_en=fake_local["en"].word(),
                    description=fake_local["ar"].sentence(),
                    description_en=fake_local["en"].sentence(),
                )
                product.categories.set(
                    random.sample(list(categories), random.randint(1, 3))
                )
                product.save()
            except IntegrityError:
                continue

    def seed_product_units(self):
        products = Product.objects.all()
        units = Unit.objects.all()

        for product in products:
            for _ in range(2):
                try:
                    product_unit = ProductUnit.objects.create(
                        product=product,
                        unit=random.choice(units),
                        cost=fake.random_number(digits=4, fix_len=True),
                        price=fake.random_number(digits=4, fix_len=True),
                        original_price=fake.random_number(digits=5, fix_len=True),
                        serial_number=fake.unique.uuid4(),
                        quantity=fake.random_int(min=10, max=100),
                        barcodes=[
                            fake.random_int(min=1000000000000, max=9999999999999)
                        ],
                        number=random.randint(10000, 999999),
                    )
                except IntegrityError:
                    continue

    def seed_product_prices(self):
        product_units = ProductUnit.objects.all()
        pricing_groups = PricingGroup.objects.all()

        for product_unit in product_units:
            for _ in range(2):
                try:
                    ProductPrice.objects.create(
                        product=product_unit,
                        pricing_group=random.choice(pricing_groups),
                        price=fake.random_number(digits=4, fix_len=True),
                        original_price=fake.random_number(digits=5, fix_len=True),
                        number=random.randint(10000, 999999),
                    )
                except IntegrityError:
                    continue
