from django.contrib.gis.db import models
from . import BranchUser, BranchUserManager


class PreparerManager(BranchUserManager):
    pass


class Preparer(BranchUser):
    admin = models.ForeignKey(BranchUser, on_delete=models.SET_NULL, related_name='preparers', blank=True, null=True)
    objects = PreparerManager()
