from django.contrib.gis.db import models
from . import BranchUser, BranchUserManager


class StaffManager(BranchUserManager):
    pass


class Staff(BranchUser):
    admin = models.ForeignKey(BranchUser, on_delete=models.SET_NULL, related_name='staffs', blank=True, null=True)
    objects = StaffManager()
