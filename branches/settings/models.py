from django.db import models
from branches.models import Branch
from core.settings.models import GeneralSettings


class BranchSettings(GeneralSettings):
    """Branch Setting model
    This model contain all settings related to a branch
    """
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='settings')
