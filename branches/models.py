import uuid

from celery.bin.multi import multi
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from parler.models import TranslatedFields
from phonenumber_field.modelfields import PhoneNumberField

from core.base.models import TimeStampedModel

User = get_user_model()


class Branch(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        REVIEWING = "REVIEWING", _("Reviewing")
        INACTIVE = "INACTIVE", _("Inactive")
        BLOCKED = "BLOCKED", _("Blocked")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Branch"), max_length=100)
    serial_number = models.CharField(_("Serial Number"), max_length=15)
    country = models.ForeignKey("settings.Country", on_delete=models.CASCADE)
    region = models.ForeignKey("settings.Region", on_delete=models.CASCADE)
    city = models.ForeignKey("settings.City", on_delete=models.CASCADE)

    phone_number = PhoneNumberField(_("Phone Number"), blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="own_branches"
    )

    location = models.PointField(_("Location"))
    zones = models.ManyToManyField(
        "settings.GeographicalZone",
        through="BranchServiceZone",
        related_name="branches",
        blank=True,
    )

    license = models.CharField(_("License"), max_length=100)
    license_file = models.FileField(_("License File"), upload_to="licenses")

    commercial_register = models.CharField(_("Commercial Register"), max_length=100)
    commercial_register_file = models.FileField(
        _("Commercial Register"), upload_to="commercial_registers"
    )

    tax_number = models.CharField(_("Tax Number"), max_length=100)
    tax_file = models.FileField(_("Tax File"), upload_to="tax_files")

    iban = models.CharField(_("IBAN"), max_length=100)
    iban_number = models.CharField(_("IBAN Number"), max_length=100)
    iban_file = models.FileField(_("IBAN File"), upload_to="iban_files")

    def __str__(self) -> str:
        return f"{self.name}"


class BranchServiceZone(TimeStampedModel):
    class DeliveryType(models.TextChoices):
        FAST = "FAST", _("Fast")
        SCHEDULED = "SCHEDULED", _("Scheduled")
        BOTH = "BOTH", _("Both")

    class ZoneType(models.TextChoices):
        ALL_TIME = "ALL_TIME", _("All Time")
        CUSTOM_TIME = "CUSTOM_TIME", _("Custom Time")

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")
        PENDING = "PENDING", _("Pending")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=100)
    name_en = models.CharField(_("English Name"), max_length=100, null=True, blank=True)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    zone = models.ForeignKey("settings.GeographicalZone", on_delete=models.CASCADE)
    delivery_type = models.CharField(
        choices=DeliveryType.choices, max_length=20, default=DeliveryType.BOTH
    )
    zone_type = models.CharField(
        choices=ZoneType.choices, max_length=20, default=ZoneType.ALL_TIME
    )
    status = models.CharField(
        choices=Status.choices, max_length=20, default=Status.PENDING
    )

    def __str__(self):
        return f"{self.branch.name} - {self.area.name}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if (
            hasattr(self.zone, "parent")
            and hasattr(self.zone, "zone_polygon")
            and hasattr(getattr(self.zone, "parent"), "zone_polygon")
        ):
            if not self.zone.parent.zone_polygon.contains(self.zone.zone_polygon):
                raise ValidationError(
                    _("The zone must be within the parent zone's boundaries.")
                )


class DeliveryTimeSlot(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")
        PENDING = "PENDING", _("Pending")

    class DaysOfWeek(models.TextChoices):
        SATURDAY = "SATURDAY", _("Saturday")
        SUNDAY = "SUNDAY", _("Sunday")
        MONDAY = "MONDAY", _("Monday")
        TUESDAY = "TUESDAY", _("Tuesday")
        WEDNESDAY = "WEDNESDAY", _("Wednesday")
        THURSDAY = "THURSDAY", _("Thursday")
        FRIDAY = "FRIDAY", _("Friday")
        ALL = "ALL", _("All")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    zone = models.ForeignKey(
        BranchServiceZone, on_delete=models.CASCADE, related_name="time_slots"
    )
    name = models.CharField(_("Name"), max_length=100)
    name_en = models.CharField(_("English Name"), max_length=100, blank=True, null=True)
    day_of_week = models.CharField(
        choices=DaysOfWeek.choices, default=DaysOfWeek.ALL, max_length=20
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        choices=Status.choices, max_length=20, default=Status.PENDING
    )

    def __str__(self):
        return f"{self.zone}"

    class Meta:
        ordering = ["day_of_week", "start_time"]


#
# class Zone(TimeStampedTranslatableModel):
#     uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='zones')
#     translations = TranslatedFields(
#         name=models.CharField(_("Name"), max_length=100)
#     )
#     zone = models.PolygonField(_("Zone"))
#     country = models.ForeignKey("settings.Country", on_delete=models.CASCADE)
#     region = models.ForeignKey("settings.Region", on_delete=models.CASCADE)
#
#     def __unicode__(self):
#         return self.title
#
#
#
# class DeliveryZone(TimeStampedTranslatableModel):
#     class ZoneType(models.TextChoices):
#         ALL_TIME = "ALL_TIME", _("All Time")
#         CUSTOM_TIME = "CUSTOM_TIME", _("Custom Time")
#
#     class DeliveryType(models.TextChoices):
#         FAST = "FAST", _("Fast")
#         SCHEDULED = "SCHEDULED", _("Scheduled")
#
#     class Status(models.TextChoices):
#         ACTIVE = "ACTIVE", _("Active")
#         INACTIVE = "INACTIVE", _("Inactive")
#         PENDING = "PENDING", _("Pending")
#
#
#     uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='delivery_zones')
#     zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='delivery_zones', null=True, blank=True)
#     translations = TranslatedFields(
#         name=models.CharField(_("Name"), max_length=100)
#     )
#     sub_regions = models.ManyToManyField('settings.SubRegion', related_name="delivery_branches", blank=True)
#     cities = models.ManyToManyField('settings.City', related_name="delivery_branches", blank=True)
#     areas = models.MultiPolygonField(_("Areas"), blank=True)
#     status = models.CharField(choices=Status.choices, max_length=20, default=Status.PENDING)
#     delivery_type = models.CharField(choices=DeliveryType.choices, max_length=20, default=DeliveryType.FAST)
#     zone_type = models.CharField(choices=ZoneType.choices, max_length=20, default=ZoneType.ALL_TIME)
#
#
#
#
#
# class TimeDeliveryZone(TimeStampedModel):
#     class Status(models.TextChoices):
#         ACTIVE = "ACTIVE", _("Active")
#         INACTIVE = "INACTIVE", _("Inactive")
#         PENDING = "PENDING", _("Pending")
#
#     class DaysOfWeek(models.TextChoices):
#         SATURDAY = "SATURDAY", _("Saturday")
#         SUNDAY = "SUNDAY", _("Sunday")
#         MONDAY = "MONDAY", _("Monday")
#         TUESDAY = "TUESDAY", _("Tuesday")
#         WEDNESDAY = "WEDNESDAY", _("Wednesday")
#         THURSDAY = "THURSDAY", _("Thursday")
#         FRIDAY = "FRIDAY", _("Friday")
#         ALL = "ALL", _("All")
#
#     uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
#     delivery_zone = models.ForeignKey(DeliveryZone, on_delete=models.CASCADE, related_name='time_delivery_zones')
#     days_of_week = models.CharField(choices=DaysOfWeek.choices, max_length=20, default=DaysOfWeek.ALL, multible=True)
#     status = models.CharField(choices=Status.choices, max_length=20, default=Status.PENDING)
#     start = models.TimeField()
#     end = models.TimeField()
