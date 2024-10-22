import uuid

from django.contrib.gis.db import models
from . import User
from django.utils.translation import gettext_lazy as _
from core.base.models import TimeStampedModel
from core.settings.models import Country, Region, SubRegion, City
from django.contrib.gis.geos import Point


class UserInfo(TimeStampedModel):
    uid = models.UUIDField(_("UID"), default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="info", verbose_name=_("User")
    )
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    gender = models.CharField(
        _("Gender"), choices=(("F", _("Female")), ("M", _("Male"))), max_length=1
    )

    def __str__(self):
        return f"{self.user.first_name}'s info"


class UserAddress(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="addresses",
        verbose_name=_("User"),
        null=True,
        blank=True,
    )
    anonymous = models.ForeignKey(
        "customers.AnonymousCustomer",
        on_delete=models.CASCADE,
        related_name="addresses",
        null=True,
        blank=True,
    )
    type = models.CharField(_("Address Type"), max_length=20, blank=True, null=True)
    name = models.CharField(_("Address Name"), max_length=255, null=True, blank=True)
    street_name = models.CharField(
        _("Street Name"), max_length=255, null=True, blank=True
    )
    name_en = models.CharField(_("Address Name"), max_length=255, null=True, blank=True)
    street_name_en = models.CharField(
        _("Street Name"), max_length=255, null=True, blank=True
    )

    street_number = models.CharField(
        _("Street Number"), max_length=20, blank=True, null=True
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name=_("Country"),
        null=True,
        blank=True,
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        verbose_name=_("Region"),
        null=True,
        blank=True,
    )
    sub_region = models.ForeignKey(
        SubRegion,
        on_delete=models.CASCADE,
        verbose_name=_("Region"),
        blank=True,
        null=True,
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name=_("City"), null=True, blank=True
    )
    location = models.PointField(_("Location"), geography=True, blank=True, null=True)
    is_default = models.BooleanField(_("Is Default"), default=False)
    images = models.ManyToManyField(
        "media.Media",
        blank=True,
        verbose_name=_("Images"),
        related_name="user_addresses",
    )

    def __str__(self):
        return f"{getattr(self.user , 'username', 'Anonymous')} - {self.street_name}, {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            UserAddress.objects.filter(user=self.user, is_default=True).update(
                is_default=False
            )
        super().save(*args, **kwargs)

    def set_location(self, latitude, longitude):
        self.location = Point(longitude, latitude)
        self.save()


class CardID(TimeStampedModel):
    uid = models.UUIDField(_("UID"), default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="card", verbose_name=_("User")
    )
    first_name = models.CharField(_("First Name"), max_length=20)
    second_name = models.CharField(
        _("Second Name"), max_length=20, blank=True, null=True
    )
    third_name = models.CharField(_("Third Name"), max_length=20, blank=True, null=True)
    family_name = models.CharField(_("Family Name"), max_length=20)
    first_name_en = models.CharField(
        _("English First Name"), max_length=20, blank=True, null=True
    )
    second_name_en = models.CharField(
        _("English Second Name"), max_length=20, blank=True, null=True
    )
    third_name_en = models.CharField(
        _("English Third Name"), max_length=20, blank=True, null=True
    )
    family_name_en = models.CharField(
        _("English Family Name"), max_length=20, blank=True, null=True
    )
    gender = models.CharField(
        _("Gender"), choices=(("F", _("Female")), ("M", _("Male"))), max_length=1
    )
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    place_of_birth = models.CharField(
        _("Place of Birth"), max_length=20, blank=True, null=True
    )
    date_of_end = models.DateField(_("Date of End"), blank=True, null=True)
    number = models.CharField(_("Card Number"), max_length=20, unique=True)
    front_image = models.ImageField(
        _("Front Image"), upload_to="cards/", blank=True, null=True
    )
    back_image = models.ImageField(
        _("Back Image"), upload_to="cards/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.family_name}"
