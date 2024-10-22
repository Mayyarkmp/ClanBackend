from django.contrib.gis.db import models
from core.settings.models import GeneralSettings
from users.models import User


class UserSettings(GeneralSettings):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settings')