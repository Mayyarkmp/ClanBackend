import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.models import Session
from users.models import UserManager, User
from django.utils.crypto import get_random_string
from core.base.models import TimeStampedModel


class CustomerManager(UserManager):
    pass


class Customer(User):
    online = models.BooleanField(default=False)
    favorites = models.ManyToManyField(
        "products.Product", blank=True, related_name="customers_favorites"
    )

    objects = CustomerManager()

    @property
    def type(self):
        return "customer"


class AnonymousCustomer(TimeStampedModel):
    fingerprint = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True
    )
    sessions = models.ManyToManyField(Session, blank=True)
    favorites = models.ManyToManyField(
        "products.Product", blank=True, related_name="anonymous_favorites"
    )

    @property
    def id(self):
        return self.fingerprint


class BrowsingKey(TimeStampedModel):
    class DeliveryType(models.TextChoices):
        FAST = "FAST", _("Fast")
        SCHEDULED = "SCHEDULED", _("Scheduled")

    key = models.CharField(max_length=24, primary_key=True)
    address = models.ForeignKey(
        "users.UserAddress", on_delete=models.CASCADE, blank=True, null=True
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    anonymous = models.ForeignKey(
        AnonymousCustomer, on_delete=models.CASCADE, blank=True, null=True
    )
    delivery_type = models.CharField(
        choices=DeliveryType.choices, default=DeliveryType.FAST, max_length=10
    )
    branch = models.ForeignKey(
        "branches.Branch", on_delete=models.CASCADE, blank=True, null=True
    )
    zone = models.ForeignKey(
        "settings.GeographicalZone", on_delete=models.CASCADE, blank=True, null=True
    )

    def _generate_key(self):
        return get_random_string(
            24, "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self._generate_key()
        super(BrowsingKey, self).save(*args, **kwargs)

    @property
    def pricing_group(self):
        if self.zone:
            return getattr(self.zone, "pricing_group")
        return None
