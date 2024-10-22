import uuid
from core.base.models import TimeStampedModel
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

class SEOSettings(TimeStampedModel):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    is_draft = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    title = models.CharField(_("Title"),max_length=255)
    description = models.TextField(_("Description"),blank=True)
    image = models.ForeignKey(
        'media.Media',
        verbose_name=_("Image"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seo_images"
    )
    title_en = models.CharField(_("English Title"),max_length=255, blank=True, null=True)
    description_en = models.TextField(_("English Description"),blank=True)
    image_en = models.ForeignKey(
        'media.Media',
        verbose_name=_("English Image"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seo_images_en"
    )

    def __str__(self):
        return f'{self.title}'
