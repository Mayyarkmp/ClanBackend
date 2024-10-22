import random
import uuid
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point, Polygon, LinearRing
from django.db.utils import IntegrityError
from faker import Faker
from core.settings.models import Country, Region, City, GeographicalZone
from branches.models import Branch, BranchServiceZone, DeliveryTimeSlot
from users.models import User

fake = Faker()
fake_local = {"ar": Faker(["ar"]), "en": Faker(["en"])}


class Command(BaseCommand):
    """Seed Branches, BranchServiceAreas, DeliveryTimeSlots, and GeographicAreas"""

    help = "Seed the database with initial data for Branches, Service Areas, Delivery Time Slots, and Geographic Areas."

    def handle(self, *args, **kwargs):
        count = kwargs.get("count", 25)  # Default to 25 records per model
        self.seed_geographic_zones(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded geographic areas!"))
        self.seed_branches(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded branches!"))
        self.seed_branch_service_areas(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded branch service areas!"))
        self.seed_delivery_time_slots(count)
        self.stdout.write(self.style.SUCCESS("Successfully seeded delivery time slots!"))

    def seed_geographic_zones(self, count):
        """Create fake geographic areas"""
        countries = Country.objects.all()
        regions = Region.objects.all()
        cities = City.objects.all()

        for _ in range(count):
            try:
                coords = [
                    (fake.longitude(), fake.latitude()),
                    (fake.longitude(), fake.latitude()),
                    (fake.longitude(), fake.latitude()),
                    (fake.longitude(), fake.latitude()),
                    (fake.longitude(), fake.latitude())
                ]

                ring = LinearRing(coords + [coords[0]])
                polygon = Polygon(ring)

                geographic_zones = GeographicalZone.objects.create(
                    uid=uuid.uuid4(),
                    country=random.choice(countries),
                    region=random.choice(regions),
                    city=random.choice(cities),
                    polygon=polygon,  # تعيين الـ polygon
                )


                geographic_zones.save()

            except IntegrityError:
                continue

    def seed_branches(self, count):
        """Create fake branches"""
        for _ in range(count):
            try:
                branch = Branch.objects.create(
                    uid=uuid.uuid4(),
                    name=fake_local["en"].company(),
                    serial_number=fake.bothify(text="??-#####"),
                    email=fake.email(),
                    owner=random.choice(User.objects.all()),
                    location=Point(float(fake.longitude()), float(fake.latitude())),
                    license=fake.bothify(text="LC-#####"),
                    commercial_register=fake.bothify(text="CR-#####"),
                    tax_number=fake.bothify(text="TN-#####"),
                    iban=fake.iban(),
                    iban_number=fake.bban(),
                    created_at=timezone.now(),
                    updated_at=timezone.now(),
                    country=random.choice(Country.objects.all()),
                    region=random.choice(Region.objects.all()),
                    city=random.choice(City.objects.all()),
                )
                branch.save()
            except IntegrityError:
                continue

    def seed_branch_service_areas(self, count):
        """Create fake branch service areas"""
        branches = Branch.objects.all()
        geographical_zones = GeographicalZone.objects.all()
        for _ in range(count):
            try:
                BranchServiceZone.objects.create(
                    uid=uuid.uuid4(),
                    branch=random.choice(branches),
                    zone=random.choice(geographical_zones),
                    delivery_type=random.choice(['FAST', 'SCHEDULED', 'BOTH']),
                    zone_type=random.choice(['ALL_TIME', 'CUSTOM_TIME']),
                    status=random.choice(['ACTIVE', 'INACTIVE', 'PENDING']),
                    name=fake_local["ar"].company(),
                    name_en=fake_local["en"].company(),
                )
            except IntegrityError:
                continue

    def seed_delivery_time_slots(self, count):
        """Create fake delivery time slots"""
        service_areas = BranchServiceZone.objects.all()
        days_of_week = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'ALL']
        for _ in range(count):
            try:
                DeliveryTimeSlot.objects.create(

                    zone=random.choice(service_areas),
                    day_of_week=random.choice(days_of_week),  # هنا تم استخدام القيم النصية للأيام
                    start_time=fake.time(),
                    end_time=fake.time(),
                    status=random.choice(['ACTIVE', 'INACTIVE', 'PENDING']),
                    name=fake_local["ar"].company(),
                    name_en=fake_local["en"].company(),
                )
            except IntegrityError:
                continue
