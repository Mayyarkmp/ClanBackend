import uuid

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from cities_light.abstract_models import (
    AbstractCity,
    AbstractCountry,
    AbstractRegion,
    AbstractSubRegion,
)
from cities_light.receivers import connect_default_signals

from products.models import PricingGroup


class Country(AbstractCountry):
    is_supported = models.BooleanField(_("Is Supported"), default=True)
    polygon = models.PolygonField(_("Country Area"), null=True, blank=True)


connect_default_signals(Country)


class Region(AbstractRegion):
    is_supported = models.BooleanField(_("Is Supported"), default=True)
    polygon = models.PolygonField(_("Region Area"), null=True, blank=True)


connect_default_signals(Region)


class SubRegion(AbstractSubRegion):
    is_supported = models.BooleanField(_("Is Supported"), default=True)
    polygon = models.PolygonField(_("SubRegion Area"), null=True, blank=True)


connect_default_signals(SubRegion)


class City(AbstractCity):
    is_supported = models.BooleanField(_("Is Supported"), default=True)
    polygon = models.PolygonField(_("City Area"), null=True, blank=True)


connect_default_signals(City)


class GeographicalZone(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")
        PENDING = "PENDING", _("Pending")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    pricing_group = models.ForeignKey(
        PricingGroup, on_delete=models.CASCADE, null=True, blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True
    )
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    subregion = models.ForeignKey(
        SubRegion, on_delete=models.CASCADE, null=True, blank=True
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    polygon = models.PolygonField(_("Geographic Area"), null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_zones",
        null=True,
        blank=True,
    )
    status = models.CharField(
        choices=Status.choices, max_length=20, default=Status.PENDING
    )

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if not any(
            [self.country, self.region, self.subregion, self.city, self.polygon]
        ):
            raise ValidationError(
                _(
                    "You must specify at least one geographic area or draw a custom area on the map."
                )
            )

    @property
    def zone_polygon(self):
        if self.polygon:
            return self.polygon
        elif self.city and hasattr(self.city, "polygon"):
            return getattr(self.city, "polygon")
        elif self.subregion and hasattr(self.subregion, "polygon"):
            return getattr(self.subregion, "polygon")
        elif self.region and hasattr(self.region, "polygon"):
            return getattr(self.region, "polygon")
        elif self.country and hasattr(self.country, "polygon"):
            return getattr(self.country, "polygon")
        else:
            return None
