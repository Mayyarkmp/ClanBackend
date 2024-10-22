from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields
import uuid
from core.base.models import TimeStampedModel


class DeliveryTypeContents(TimeStampedModel):
    class DeliveryType(models.TextChoices):
        FAST = "FAST", _("Fast")
        SCHEDULED = "SCHEDULED", _("Scheduled")

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    type = models.CharField(
        max_length=10, choices=DeliveryType.choices, default=DeliveryType.FAST
    )

    name = models.CharField(_("Name"), max_length=50)
    short_description = models.TextField(_("Short Description"), blank=True)
    description = models.TextField(_("Description"), blank=True)
    name_en = models.CharField(_("English Name"), max_length=50, null=True, blank=True)
    short_description_en = models.TextField(_("English Short Description"), blank=True)
    description_en = models.TextField(_("English Description"), blank=True)
    image = models.ForeignKey(
        "media.Media", on_delete=models.SET_NULL, null=True, blank=True
    )

    is_draft = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Delivery Type Content")
        verbose_name_plural = _("Delivery Type Contents")
        constraints = [
            models.UniqueConstraint(
                fields=["type"],
                name="unique_delivery_type_active_content",
                condition=models.Q(is_deleted=False, is_draft=False, is_default=True),
            )
        ]

    def save(self, *args, **kwargs):
        if self.is_default:
            self.__class__.objects.filter(
                is_default=True, is_deleted=False, is_draft=False
            ).update(is_default=False)
        super(DeliveryTypeContents, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Pages(TimeStampedModel):
    class TypeApp(models.TextChoices):
        MOBILE = "MOBILE", _("Mobile")
        WEB = "WEB", _("Web")

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    type = models.CharField(choices=TypeApp.choices, max_length=50)
    title = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(
        _("English Title"), max_length=255, null=True, blank=True
    )
    slug = models.SlugField(max_length=255)
    is_draft = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type", "slug"], name="unique_type_slug")
        ]
