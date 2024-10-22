import uuid

from core.base.models import TimeStampedModel
from . import BranchUser, BranchUserManager
from django.contrib.gis.db import models


class DeliveryManager(BranchUserManager):
    pass


class Delivery(BranchUser):
    admin = models.ForeignKey(BranchUser, on_delete=models.SET_NULL, related_name='deliveries', blank=True, null=True)
    objects = DeliveryManager()




