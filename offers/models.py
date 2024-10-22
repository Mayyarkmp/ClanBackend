from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
import uuid
from core.base.models import TimeStampedModel


class Promotion(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    start_date = models.DateTimeField(_("Start Date"), null=True, blank=True)
    end_date = models.DateTimeField(_("End Date"), null=True, blank=True)
    free_delivery = models.BooleanField(_("Free Delivery"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_draft = models.BooleanField(default=True)

    def get_conditions(self):
        return getattr(getattr(self, "conditions"), "all")

    class Meta:
        abstract = True


class PromotionTimeSlot(TimeStampedModel):
    promotion_condition = models.ForeignKey(
        "PromotionCondition", on_delete=models.CASCADE, related_name="time_slots"
    )
    day = models.DateField(_("Day"))
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))

    def __str__(self):
        return f"{self.start_time} - {self.end_time} for {self.promotion_condition}"

    class Meta:
        verbose_name = _("Promotion Time Slot")
        verbose_name_plural = _("Promotion Time Slots")


class PromotionRegionLimit(models.Model):
    promotion_condition = models.ForeignKey(
        "PromotionCondition", on_delete=models.CASCADE, related_name="region_limits"
    )
    region = models.ForeignKey(
        "settings.Region", on_delete=models.CASCADE, related_name="promotion_limits"
    )
    max_quantity = models.PositiveIntegerField(_("Max Quantity"), null=True, blank=True)
    max_customers = models.PositiveIntegerField(
        _("Max Customers"), null=True, blank=True
    )

    class Meta:
        unique_together = (("promotion_condition", "region"),)
        verbose_name = _("Promotion Region Limit")
        verbose_name_plural = _("Promotion Region Limits")

    def __str__(self):
        return f"{self.promotion_condition} - {self.region}"


class PromotionBranchLimit(TimeStampedModel):
    promotion_condition = models.ForeignKey(
        "PromotionCondition", on_delete=models.CASCADE, related_name="branch_limits"
    )
    branch = models.ForeignKey(
        "branches.Branch", on_delete=models.CASCADE, related_name="promotion_limits"
    )
    max_quantity = models.PositiveIntegerField(_("Max Quantity"), null=True, blank=True)
    max_customers = models.PositiveIntegerField(
        _("Max Customers"), null=True, blank=True
    )

    class Meta:
        unique_together = (("promotion_condition", "branch"),)
        verbose_name = _("Promotion Branch Limit")
        verbose_name_plural = _("Promotion Branch Limits")

    def __str__(self):
        return f"{self.promotion_condition} - {self.branch}"


class PromotionCondition(TimeStampedModel):
    class DeliveryType(models.TextChoices):
        FAST = "FAST", _("Fast")
        SCHEDULED = "SCHEDULED", _("Scheduled")
        BOTH = "BOTH", _("Both")

    class Platform(models.TextChoices):
        WEB = "WEB", _("Web")
        MOBILE = "MOBILE", _("Mobile")
        BOTH = "BOTH", _("Both")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    min_cart_total = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        null=True,
        blank=True,
        verbose_name=_("Minimum Cart Total"),
    )
    start_date = models.DateTimeField(_("Start Date"), null=True, blank=True)
    end_date = models.DateTimeField(_("End Date"), null=True, blank=True)
    max_uses_per_customer = models.PositiveIntegerField(
        _("Max Uses Per Customer"), null=True, blank=True
    )
    max_views_per_customer = models.PositiveIntegerField(
        _("Max Views Per Customer"), null=True, blank=True
    )
    applicable_countries = models.ManyToManyField(
        "settings.Country", verbose_name=_("Applicable Countries"), blank=True
    )
    applicable_regions = models.ManyToManyField(
        "settings.Region", verbose_name=_("Applicable Regions"), blank=True
    )
    applicable_sub_regions = models.ManyToManyField(
        "settings.SubRegion", verbose_name=_("Applicable SubRegions"), blank=True
    )
    applicable_cities = models.ManyToManyField(
        "settings.City", verbose_name=_("Applicable Cities"), blank=True
    )
    applicable_branches = models.ManyToManyField(
        "branches.Branch", verbose_name=_("Applicable Branches"), blank=True
    )
    applicable_delivery_types = models.CharField(
        choices=DeliveryType.choices, max_length=10, default=DeliveryType.BOTH
    )
    applicable_platforms = models.CharField(
        choices=Platform.choices, max_length=10, default=Platform.BOTH
    )

    included_products = models.ManyToManyField(
        "products.Product",
        verbose_name=_("Included Products"),
        related_name="included_in_promotions",
        blank=True,
    )
    excluded_products = models.ManyToManyField(
        "products.Product",
        verbose_name=_("Excluded Products"),
        related_name="excluded_from_promotions",
        blank=True,
    )
    included_groups = models.ManyToManyField(
        "products.Group",
        verbose_name=_("Included Groups"),
        related_name="included_in_promotions",
        blank=True,
    )
    excluded_groups = models.ManyToManyField(
        "products.Group",
        verbose_name=_("Excluded Groups"),
        related_name="excluded_from_promotions",
        blank=True,
    )
    included_categories = models.ManyToManyField(
        "products.Category",
        verbose_name=_("Included Categories"),
        related_name="included_in_promotions",
        blank=True,
    )
    excluded_categories = models.ManyToManyField(
        "products.Category",
        verbose_name=_("Excluded Categories"),
        related_name="excluded_from_promotions",
        blank=True,
    )
    included_brands = models.ManyToManyField(
        "products.Brand",
        verbose_name=_("Included Brands"),
        related_name="included_in_promotions",
        blank=True,
    )

    excluded_brands = models.ManyToManyField(
        "products.Brand",
        verbose_name=_("Excluded Brands"),
        related_name="excluded_from_promotions",
        blank=True,
    )

    included_suppliers = models.ManyToManyField(
        "products.Supplier",
        verbose_name=_("Included Suppliers"),
        related_name="included_in_promotions",
        blank=True,
    )
    excluded_suppliers = models.ManyToManyField(
        "products.Supplier",
        verbose_name=_("Excluded Suppliers"),
        related_name="excluded_from_promotions",
        blank=True,
    )
    included_payment_services = models.ManyToManyField(
        "settings.PaymentService",
        verbose_name=_("Included Payment Services"),
        related_name="included_in_promotions",
        blank=True,
    )
    excluded_payment_services = models.ManyToManyField(
        "settings.PaymentService",
        verbose_name=_("Excluded Payment Services"),
        related_name="excluded_from_promotions",
        blank=True,
    )

    max_total_quantity = models.PositiveIntegerField(
        _("Max Total Quantity"), null=True, blank=True
    )
    max_total_customers = models.PositiveIntegerField(
        _("Max Total Customers"), null=True, blank=True
    )

    def __str__(self):
        return f"Conditions for {self.content_object}"

    class Meta:
        verbose_name = _("Promotion Condition")
        verbose_name_plural = _("Promotion Conditions")


class PromotionUsage(TimeStampedModel):
    promotion_condition = models.ForeignKey(
        "PromotionCondition", on_delete=models.CASCADE, related_name="usages"
    )
    customer = models.ForeignKey(
        "customers.Customer", on_delete=models.CASCADE, null=True, blank=True
    )
    anonymous = models.ForeignKey(
        "customers.AnonymousCustomer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    branch = models.ForeignKey(
        "branches.Branch", on_delete=models.CASCADE, null=True, blank=True
    )
    region = models.ForeignKey(
        "settings.Region", on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    used_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _("Promotion Usage")
        verbose_name_plural = _("Promotion Usages")

    def __str__(self):
        return (
            f"Usage of {self.promotion_condition} by {self.customer} at {self.used_at}"
        )


class PromotionAnalytics(TimeStampedModel):
    class EventType(models.TextChoices):
        IMPRESSION = "IMPRESSION", _("Impression")
        CLICK = "CLICK", _("Click")
        ORDER = "ORDER", _("Order")
        PURCHASE = "PURCHASE", _("Purchase")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    event_type = models.CharField(
        _("Event Type"), max_length=20, choices=EventType.choices
    )
    customer = models.ForeignKey(
        "customers.Customer", on_delete=models.CASCADE, null=True, blank=True
    )
    anonymous = models.ForeignKey(
        "customers.AnonymousCustomer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    branch = models.ForeignKey(
        "branches.Branch", on_delete=models.CASCADE, null=True, blank=True
    )

    zone = models.ForeignKey(
        "settings.GeographicalZone", on_delete=models.CASCADE, null=True, blank=True
    )

    platform = models.CharField(_("Platform"), max_length=20, null=True, blank=True)
    device = models.CharField(_("Device"), max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    browsing_key = models.ForeignKey(
        "customers.BrowsingKey", on_delete=models.CASCADE, null=True, blank=True
    )
    session_id = models.CharField(
        _("Session ID"), max_length=255, null=True, blank=True
    )
    ip_address = models.GenericIPAddressField(_("IP Address"), null=True, blank=True)
    user_agent = models.CharField(
        _("User Agent"), max_length=255, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Promotion Analytics")
        verbose_name_plural = _("Promotion Analytics")

    def __str__(self):
        return f"{self.event_type} - {self.content_object or ''} at {self.timestamp}"
