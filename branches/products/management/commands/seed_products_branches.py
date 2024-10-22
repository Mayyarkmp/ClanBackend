"""
    Create Fake data for products in branches
"""

import random
import uuid
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.db.utils import IntegrityError

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
from branches.users.models import BranchUser, Preparer
from core.settings.models import Country, Region, City
from products.models import Product as GlobalProduct, Unit
from users.models import User

fake = Faker()
fake_local = {"ar": Faker(["ar"]), "en": Faker(["en"])}

LANGUAGES = ["en", "ar"]


class Command(BaseCommand):
    """Seed Branches Products"""

    help = "Seed the database with initial data for Groups, Suppliers, Categories, Products, Units, Pricing Groups, Costs, Prices, and Barcodes."
    p = Point([32, 45])

    def handle(self, *args, **kwargs):
        count = kwargs.get("count", 5)
        self.seed_users(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded users!"))
        self.seed_branches(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded branches!"))
        self.seed_sub_branch_user(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded branch users!"))
        self.seed_sub_branch_preparer(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded branch preparer!"))
        self.seed_pricing_group(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded pricing_group!"))
        self.seed_product(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded product!"))
        self.seed_primary_shelf(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded primary_shelf!"))
        self.seed_sub_shelf()
        self.stdout.write(self.style.SUCCESS("Successfully seeded sub_shelf!"))
        self.seed_shelf()
        self.stdout.write(self.style.SUCCESS("Successfully seeded shelf!"))
        self.seed_product_quantity()
        self.stdout.write(self.style.SUCCESS("Successfully seeded product_quantity!"))
        self.seed_product_cost()
        self.stdout.write(self.style.SUCCESS("Successfully seeded product_cost!"))
        self.seed_product_prict()
        self.stdout.write(self.style.SUCCESS("Successfully seeded product_prict!"))
        self.seed_product_change_request()
        self.stdout.write(
            self.style.SUCCESS("Successfully seeded product_change_request!")
        )
        self.seed_product_transfer_request()
        self.stdout.write(
            self.style.SUCCESS("Successfully seeded product_transfer_request!")
        )
        self.seed_product_supply_request()
        self.stdout.write(
            self.style.SUCCESS("Successfully seeded product_supply_request!")
        )
        self.stdout.write(self.style.SUCCESS("Successfully seeded the database!"))

    def seed_users(self, count):
        """Seed owner branches"""
        for _ in range(count):
            m = User.objects.create(
                email=fake.email(),
                username=f"{fake.user_name()}{fake.random_int(min=100, max=999)}",
            )
            m.set_password("password")
            m.save()

    def seed_branches(self, count):
        """branches"""
        for _ in range(count):
            branch = Branch.objects.create(
                uid=uuid.uuid4(),
                name=fake_local["ar"].name(),
                email=fake.email(),
                serial_number=fake.bothify(text="??-#####"),
                license=fake.bothify(text="LC-#####"),
                commercial_register=fake.bothify(text="CR-#####"),
                tax_number=fake.bothify(text="TN-#####"),
                location=self.p,
                owner=random.choice(User.objects.all()),
                created_at=timezone.now(),
                updated_at=timezone.now(),
                country=random.choice(Country.objects.all()),
                region=random.choice(Region.objects.all()),
                city=random.choice(City.objects.all()),
            )
            branch.save()

    def seed_sub_branch_user(self, count):
        """sub_branch_user"""
        branches = Branch.objects.all()
        for b in branches:
            for _ in range(count):
                try:
                    u = BranchUser.objects.create(
                        username=f"{fake.user_name()}{fake.random_int(min=100, max=999)}",
                        email=fake.email(),
                        branch=b,
                        location=self.p,
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    )
                    u.set_password("password")
                    u.save()
                except IntegrityError:
                    continue

    def seed_sub_branch_preparer(self, count):
        """sub_branch_user"""
        branches = Branch.objects.all()
        for b in branches:
            for _ in range(count):
                try:
                    u = Preparer.objects.create(
                        username=f"{fake.user_name()}{fake.random_int(min=100, max=999)}",
                        email=fake.email(),
                        branch=b,
                        location=self.p,
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    )
                    u.set_password("password")
                    u.save()
                except IntegrityError:
                    continue

    def seed_pricing_group(self, count):
        """pricing_group"""
        branches = Branch.objects.all()
        for b in branches:
            for _ in range(count):
                try:
                    PricingGroup.objects.create(
                        uid=uuid.uuid4(),
                        codename=f"{fake.slug()}{fake.random_int(min=100, max=999)}",
                        branch=b,
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        name=fake_local["ar"].name(),
                        name_en=fake_local["en"].name(),
                    )
                except IntegrityError:
                    continue

    def seed_product(self, count):
        """product"""
        branches = Branch.objects.all()
        for b in branches:
            for _ in range(count):
                try:
                    Product.objects.create(
                        uid=uuid.uuid4(),
                        sq=fake.bothify(text="??-#####"),
                        number=fake.random_int(min=9999, max=99999),
                        branch=b,
                        product=random.choice(GlobalProduct.objects.all()),
                        type=random.choice(
                            [Product.Types.PRIMARY, Product.Types.SECONDARY]
                        ),
                        status=random.choice(
                            [Product.Status.ACTIVE, Product.Status.INACTIVE]
                        ),
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    )
                except IntegrityError:
                    continue

    def seed_primary_shelf(self, count):
        """primary_shelf"""
        branches = Branch.objects.all()
        for b in branches:
            for _ in range(count):
                try:
                    PrimaryShelf.objects.create(
                        uid=uuid.uuid4(),
                        codename=f"{fake.slug()}{fake.random_int(min=100, max=999)}",
                        index=fake.random_int(min=1, max=100),
                        branch=b,
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        name=fake_local["ar"].name(),
                        name_en=fake_local["en"].name(),
                    )

                except IntegrityError:
                    continue

    def seed_sub_shelf(self):
        """sub_shelf"""
        branches = Branch.objects.all()
        for b in branches:
            primary_shelves = PrimaryShelf.objects.filter(branch=b)
            for ps in primary_shelves:
                try:
                    SubShelf.objects.create(
                        uid=uuid.uuid4(),
                        codename=f"{fake.slug()}{fake.random_int(min=100, max=999)}",
                        index=fake.random_int(min=1, max=100),
                        # branch=b,
                        primary_shelf=ps,
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        name=fake_local["ar"].name(),
                        name_en=fake_local["en"].name(),
                    )

                except IntegrityError:
                    continue

    def seed_shelf(self):
        """shelf"""
        branches = Branch.objects.all()
        print(len(branches))
        for b in branches:
            primary_shelves = PrimaryShelf.objects.filter(branch=b)
            products = Product.objects.filter(branch=b)
            for ps in primary_shelves:
                sub_shelves = SubShelf.objects.filter(primary_shelf=ps)
                for ss in sub_shelves:
                    try:
                        ps = Shelf.objects.create(
                            uid=uuid.uuid4(),
                            codename=f"{fake.slug()}{fake.random_int(min=10000, max=99999)}",
                            index=fake.random_int(min=1, max=100000),
                            sub_shelf=ss,
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            supervisor=random.choice(Preparer.objects.all()),
                            name=fake_local["ar"].name(),
                            name_en=fake_local["en"].name(),
                        )
                        ps.products.set(
                            random.choices(
                                products,
                                k=fake.random_int(min=1, max=20),
                            ),
                        )
                        ps.save()
                    except IntegrityError:
                        print(12)
                        continue

    def seed_product_quantity(self):
        """product_quantity"""
        branches = Branch.objects.all()
        for b in branches:
            for p in Product.objects.filter(branch=b):
                for _ in range(5):
                    try:
                        ProductQuantity.objects.create(
                            uid=uuid.uuid4(),
                            product=p,
                            quantity=fake.random_int(min=10, max=100),
                            unit=random.choice(Unit.objects.all()),
                        )
                    except IntegrityError:
                        continue

    def seed_product_cost(self):
        """product_cost"""
        branches = Branch.objects.all()
        for b in branches:
            for p in Product.objects.filter(branch=b):
                for _ in range(5):
                    try:
                        ProductCost.objects.create(
                            uid=uuid.uuid4(),
                            product=p,
                            cost_currency="SAR",
                            cost=fake.random_int(min=10, max=100),
                            unit=random.choice(Unit.objects.all()),
                        )
                    except IntegrityError:
                        continue

    def seed_product_prict(self):
        """product_prict"""
        branches = Branch.objects.all()
        for b in branches:
            for p in Product.objects.filter(branch=b):
                for _ in range(5):
                    try:
                        ProductPrice.objects.create(
                            uid=uuid.uuid4(),
                            product=p,
                            price_currency="SAR",
                            price=fake.random_int(min=10, max=100),
                            unit=random.choice(Unit.objects.all()),
                            pricing_group=random.choice(
                                PricingGroup.objects.filter(branch=b)
                            ),
                        )

                    except IntegrityError:
                        continue

    def seed_product_change_request(self):
        """Seed Product Change Request"""
        branches = Branch.objects.all()
        for b in branches:
            for p in Product.objects.filter(branch=b):
                ProductChangeStateRequest.objects.create(
                    uid=uuid.uuid4(),
                    product=p,
                    creator=random.choice(BranchUser.objects.filter(branch=b)),
                    status=random.choice(
                        [
                            ProductChangeStateRequest.Status.ACCEPTED,
                            ProductChangeStateRequest.Status.REVIEWING,
                            ProductChangeStateRequest.Status.REJECTED,
                        ]
                    ),
                    request_type=random.choice(
                        [
                            "ACTIVATE",
                            "DEACTIVATE",
                        ]
                    ),
                )

    def seed_product_transfer_request(self):
        """product_transfer_request"""
        branches = Branch.objects.all()
        for b in branches:
            shelves = Shelf.objects.filter(sub_shelf__primary_shelf__branch=b)
            branch_users = BranchUser.objects.filter(branch=b)
            if shelves.count() > 0:
                products = Product.objects.filter(branch=b)
                if products.count() > 0:
                    for p in products:
                        ProductTransferRequest.objects.create(
                            uid=uuid.uuid4(),
                            product=p,
                            from_shelf=random.choice(shelves),
                            to_shelf=random.choice(shelves),
                            creator=random.choice(branch_users),
                            status=random.choice(
                                [
                                    ProductChangeStateRequest.Status.ACCEPTED,
                                    ProductChangeStateRequest.Status.REVIEWING,
                                    ProductChangeStateRequest.Status.REJECTED,
                                ]
                            ),
                        )

    def seed_product_supply_request(self):
        """product_supply_request"""
        branches = Branch.objects.all()
        for b in branches:
            for p in Product.objects.filter(branch=b):
                psr = ProductSupplyRequest.objects.create(
                    uid=uuid.uuid4(),
                    product=p,
                    creator=random.choice(BranchUser.objects.filter(branch=b)),
                    supplier=random.choice(User.objects.all()),
                    supervisor=random.choice(User.objects.all()),
                    status=random.choice(
                        [
                            ProductSupplyRequest.Status.PENDING,
                            ProductSupplyRequest.Status.IN_PROGRESS,
                            ProductSupplyRequest.Status.COMPLETED,
                            ProductSupplyRequest.Status.REJECTED,
                            ProductSupplyRequest.Status.CANCELLED,
                            ProductSupplyRequest.Status.IN_TRANSIT,
                            ProductSupplyRequest.Status.ON_HOLD,
                            ProductSupplyRequest.Status.SUPPLIED,
                        ]
                    ),
                )
                for _ in range(5):
                    ProductSupplyAction.objects.create(
                        actor=random.choice(BranchUser.objects.filter(branch=b)),
                        action=random.choice(
                            [
                                ProductSupplyAction.Actions.CREATED,
                                ProductSupplyAction.Actions.UPDATED,
                                ProductSupplyAction.Actions.APPROVED,
                                ProductSupplyAction.Actions.REJECTED,
                                ProductSupplyAction.Actions.SUPPLIED,
                                ProductSupplyAction.Actions.CANCELLED,
                                ProductSupplyAction.Actions.IN_PROGRESS,
                                ProductSupplyAction.Actions.IN_TRANSIT,
                            ]
                        ),
                        request=psr,
                    )
