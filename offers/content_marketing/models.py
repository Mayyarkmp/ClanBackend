from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from offers.models import Promotion, PromotionCondition


class Advertisement(Promotion):
    class Type(models.TextChoices):
        CUSTOM = "CUSTOM", _("Custom")
        PRODUCT = "PRODUCT", _("Product")
        OFFER = "OFFER", _("Offer")

    class Shape(models.TextChoices):
        BAR = "BAR", _("Bar")
        POPUP = "POPUP", _("Popup")
        CARD = "CARD", _("Card")
        PRODUCT_CARD = "PRODUCT_CARD", _("Product Card")
        GROUP_CARD = "GROUP_CARD", _("Group Card")
        CATEGORY_CARD = "CATEGORY_CARD", _("Category Card")

    color = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.CUSTOM)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    content_en = models.TextField(blank=True, null=True)
    image = models.ForeignKey(
        "media.Media", on_delete=models.SET_NULL, null=True, blank=True
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.SET_NULL, null=True, blank=True
    )
    offer = models.ForeignKey(
        "discounts.Offer", on_delete=models.SET_NULL, null=True, blank=True
    )

    shape = models.CharField(choices=Shape.choices, max_length=50, default=Shape.BAR)
    url = models.URLField(blank=True)
    conditions = GenericRelation(PromotionCondition, related_name="advertisements")
    # TODO: Update Customizing Pages Showing
    show_in_order_summary = models.BooleanField(default=False)
    show_in_cart = models.BooleanField(default=False)
    show_in_checkout = models.BooleanField(default=False)
