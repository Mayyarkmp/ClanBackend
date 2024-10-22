from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group


ALLOWED_MODELS = ['user', 'centraluser', 'branchuser', 'manager', 'delivery', 'preparer', 'staff']




