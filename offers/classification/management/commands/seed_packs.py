import random
import uuid
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
from core.media.models import Media  # تأكد من تعديل المسار حسب الحاجة
from offers.classification.models import Pack
from products.models import (
    Group,
    Supplier,
    Category,
    Product,
    Brand,
)


fake = Faker()
fake_local = {"ar": Faker(["ar"]), "en": Faker(["en"])}


class Command(BaseCommand):
    help = "Seed the database with initial data for Groups, Suppliers, Categories, Products, Units, Pricing Groups, Costs, Prices, and Barcodes."

    def handle(self, *args, **kwargs):
        self.seed_packs()
        self.stdout.write(self.style.SUCCESS("Successfully seeded groups!"))
        self.stdout.write(self.style.SUCCESS("Successfully seeded the database!"))

    def seed_packs(self):
        for _ in range(50):
            try:
                p = Pack.objects.create(
                    name=fake_local["ar"].company(),
                    name_en=fake_local["en"].company(),
                    description=fake_local["ar"].text(),
                    description_en=fake_local["en"].text(),
                )
                p.images.set(
                    random.sample(list(Media.objects.all()), random.randint(1, 3))
                )
                p.default_image = random.choice(p.images.all()).file.url
                p.products.set(
                    random.sample(list(Product.objects.all()), random.randint(0, 20))
                )
                p.groups.set(
                    random.sample(list(Group.objects.all()), random.randint(0, 3))
                )
                p.categories.set(
                    random.sample(list(Category.objects.all()), random.randint(0, 3))
                )
                p.brands.set(
                    random.sample(list(Brand.objects.all()), random.randint(0, 3))
                )
                p.suppliers.set(
                    random.sample(list(Supplier.objects.all()), random.randint(0, 3))
                )
                p.save()
            except IntegrityError:
                continue
