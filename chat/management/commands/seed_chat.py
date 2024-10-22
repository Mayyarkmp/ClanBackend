"""
    Create Fake data for products in branches
"""

import random
import uuid
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from djmoney.money import Money

from faker import Faker
from chat.models import Room, Message
from users.models import User, UserAddress
fake = Faker()
fake_local = {"ar": Faker(["ar"]), "en": Faker(["en"])}

LANGUAGES = ["en", "ar"]


class Command(BaseCommand):
    """Seed Branches Products"""

    help = "Seed the database with initial data for Groups, Suppliers, Categories, Products, Units, Pricing Groups, Costs, Prices, and Barcodes."
    p = Point([32, 45])

    def handle(self, *args, **kwargs):

        # for _ in range(100):
        #     u = User.objects.create(
        #         phone_number=fake.phone_number(),
        #         email=fake.email(),
        #         username=f"{fake.user_name()}{fake.random_int(min=100, max=999)}",
        #     )
        #     u.set_password("password")
        #     u.save()



        users = User.objects.all()

        for _ in range(50):
            members = random.choices(users, k=random.randint(2, 10))
            room = Room.objects.create()
            room.members.set(members)
            for _ in range(random.randint(1, 100)):
                Message.objects.create(
                    room=room,
                    sender=random.choice(users),
                    message=fake.text(max_nb_chars=100),
                    sending_datetime=timezone.now(),
                    is_sent=random.choice([True, False]),
                    is_read=random.choice([True, False]),
                    is_received=random.choice([True, False]),
                    is_edited=random.choice([True, False]),
                    location=Point(random.random(), random.random()),
                    type=random.choice(Message.Types.names),
                )
