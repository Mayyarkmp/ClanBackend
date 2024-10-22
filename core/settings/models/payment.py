from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields

from core.base.models import TimeStampedModel

class Currency(TimeStampedModel):
    code = models.CharField(max_length=3, unique=True)
    name=models.CharField(_("Name"),max_length=50, blank=True)
    name_en = models.CharField(_("English Name"),max_length=50, blank=True)

    symbol = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f"{self.code} ({self.name})"



class PaymentService(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)
    code = models.CharField(_("Code"), max_length=50, unique=True)
    data_config = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Payment Service")
        verbose_name_plural = _("Payment Services")
