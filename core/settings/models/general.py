from django.contrib.gis.db import models
from parler.models import TranslatedFields
from polymorphic.models import PolymorphicModel
from core.base.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class GeneralSettings(PolymorphicModel, TimeStampedModel):
    class Type(models.TextChoices):
        GLOBAL = "GLOBAL", _("Global")
        BRANCH = "Branch", _("Branch")
        USER = "User", _("User")
        CUSTOMER = "Customer", _("Customer")
        CENTRAL = "Central", _("Central")
        DELIVERY = "Delivery", _("Delivery")
        PREPARER = "Preparer", _("Preparer")
        STAFF = "Staff", _("Staff")
        DELIVERING = "Delivering", _("Delivering")
        PREPARING = "Preparing", _("Preparing")
        MANAGER = "Manager", _("Manager")

    class ValueType(models.TextChoices):
        TEXT = "TEXT", _("Text")
        NUMBER = "NUMBER", _("Number")
        DATE = "DATE", _("Date")
        DATETIME = "DATETIME", _("Date/Time")
        TIME = "TIME", _("Time")
        BOOLEAN = "BOOLEAN", _("Boolean")
        LOCATION = "LOCATION", _("Location")
        ZONE = "ZONE", _("Zone")
        OBJECT = "OBJECT", _("Object")

    name = (models.CharField(_("Name"), max_length=255, null=True, blank=True),)
    name_en = (
        models.CharField(_("English Name"), max_length=255, null=True, blank=True),
    )
    description = (models.TextField(_("Description Setting"), null=True, blank=True),)
    description_en = (
        models.TextField(_("English Description Setting"), null=True, blank=True),
    )

    type = models.CharField(choices=Type.choices, default=Type.GLOBAL, max_length=50)
    key = models.SlugField(max_length=100)
    value_type = models.CharField(
        choices=ValueType.choices, default=ValueType.TEXT, max_length=50
    )
    value = models.TextField()

    def __str__(self):
        return self.name + " : " + self.value
