from django.contrib.contenttypes.fields import GenericRelation
import uuid
from rest_framework.exceptions import ValidationError

from core.base.models import TimeStampedModel
from polymorphic.models import PolymorphicModel
from offers.models import PromotionCondition, Promotion
from django.db import models
from django.utils.translation import gettext_lazy as _


class Coupon(PolymorphicModel, Promotion):
    class Type(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", _("Percentage")
        AMOUNT = "AMOUNT", _("Amount")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(choices=Type.choices, max_length=50)
    code = models.CharField(_("Code"), max_length=50, unique=True)
    value = models.DecimalField(
        _("Discount Value"), max_digits=5, decimal_places=2, null=True, blank=True
    )
    conditions = GenericRelation(PromotionCondition, related_name="coupons")

    def clean(self):
        if self.type == self.Type.PERCENTAGE and not self.value:
            raise ValidationError(
                _("Discount percentage must be set for percentage type.")
            )
        if self.type == self.Type.AMOUNT and not self.value:
            raise ValidationError(_("Discount amount must be set for amount type."))

    def __str__(self):
        text = self.code or self.name or self.name_en
        return f"{text}"


class MarketingCoupon(Coupon):
    advertiser = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    commission_type = models.CharField(
        choices=Coupon.Type.choices, max_length=50, null=True, blank=True
    )
    commission_value = models.DecimalField(
        _("Advertiser Commission Percentage"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def clean(self):
        super().clean()
        if self.commission_type == self.Type.PERCENTAGE and not self.commission_value:
            raise ValidationError(
                _("Advertiser commission percentage must be set for percentage type.")
            )
        if self.commission_type == self.Type.AMOUNT and not self.commission_value:
            raise ValidationError(
                _("Advertiser commission amount must be set for amount type.")
            )


class Offer(Promotion):
    class Type(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", _("Percentage")
        AMOUNT = "AMOUNT", _("Amount")
        FREE_PRODUCT = "FREE_PRODUCT", _("Free Product")
        CASHBACK = "CASHBACK", _("Cashback")

    type = models.CharField(choices=Type.choices, max_length=50)

    work_with_coupon = models.BooleanField(_("Work with Coupon"), default=False)
    work_with_offer = models.BooleanField(_("Work with Other Offer"), default=False)
    min_purchase_amount = models.DecimalField(
        _("Min Purchase Amount"), max_digits=14, decimal_places=2, blank=True, null=True
    )
    units = models.ManyToManyField("products.Unit", related_name="offers", blank=True)
    code = models.CharField(_("Code"), max_length=50, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)

    conditions = GenericRelation(PromotionCondition, related_name="offers")

    def __str__(self):
        text = self.name or self.code
        return f"{text}"


class OfferCondition(models.Model):
    class ConditionType(models.TextChoices):
        FREE_PRODUCT = "FREE_PRODUCT", _("Free Product")
        DISCOUNT = "DISCOUNT", _("Discount")
        CASHBACK = "CASHBACK", _("Cashback")
        QUANTITY = "QUANTITY", _("Quantity")

    class BuyType(models.TextChoices):
        COUNT = "COUNT", _("Count")
        PRICE = "PRICE", _("Price")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    type = models.CharField(choices=ConditionType.choices, max_length=50)
    value = models.DecimalField(
        _("Value"), max_digits=14, decimal_places=2, null=True, blank=True
    )
    buy_type = models.CharField(
        choices=BuyType.choices, max_length=50, default=BuyType.COUNT
    )
    buy_value = models.PositiveIntegerField(_("Buy Count or Price"), default=1)
    content = models.TextField(null=True, blank=True)
    products_buy = models.ManyToManyField(
        "products.Product", blank=True, related_name="buy_conditions"
    )
    products_get = models.ManyToManyField(
        "products.Product", blank=True, related_name="get_conditions"
    )
    groups_buy = models.ManyToManyField(
        "products.Group", blank=True, related_name="group_buy_conditions"
    )
    groups_get = models.ManyToManyField(
        "products.Group", blank=True, related_name="group_get_conditions"
    )
    brands_buy = models.ManyToManyField(
        "products.Brand", blank=True, related_name="brand_buy_conditions"
    )
    brands_get = models.ManyToManyField(
        "products.Brand", blank=True, related_name="brand_get_conditions"
    )
    categories_buy = models.ManyToManyField(
        "products.Category", blank=True, related_name="category_buy_conditions"
    )
    categories_get = models.ManyToManyField(
        "products.Category", blank=True, related_name="category_get_conditions"
    )
    packs_buy = models.ManyToManyField(
        "offers_classification.Pack", blank=True, related_name="pack_buy_conditions"
    )
    packs_get = models.ManyToManyField(
        "offers_classification.Pack", blank=True, related_name="pack_get_conditions"
    )

    offer = models.ForeignKey(
        "discounts.Offer", on_delete=models.CASCADE, related_name="offer_conditions"
    )

    def __str__(self):
        return f"{self.type} - {self.value}"


class OfferImage(models.Model):
    class ImageType(models.TextChoices):
        BAR = "BAR", _("Bar")
        POPUP = "POPUP", _("Popup")
        CARD = "CARD", _("Card")
        PRODUCT_CARD = "PRODUCT_CARD", _("Product Card")
        GROUP_CARD = "GROUP_CARD", _("Group Card")
        CATEGORY_CARD = "CATEGORY_CARD", _("Category Card")

    type = models.CharField(choices=ImageType.choices, max_length=20)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    image = models.ForeignKey("media.Media", on_delete=models.CASCADE)


# class AbandonedCartOffer(Offer):
#     carts = models.ManyToManyField("orders.Cart", related_name="abandoned_cart_offers")
