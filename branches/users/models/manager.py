# from branches.models import Branch
# from branches.serializers import BranchSerializer
# from branches.users.models.branch_user import Status
# from branches.users.serializers import ManagerSerializer
# from core.base import viewsets
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import action
from .branch_user import Status
from . import BranchUser, BranchUserManager
from django.contrib.gis.db import models


# Modified
class BranchManagerManager(BranchUserManager):
    pass


class Manager(BranchUser):
    objects = BranchManagerManager()
