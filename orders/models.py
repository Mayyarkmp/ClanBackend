import uuid
import random
from django.db import connection
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from django.contrib.sessions.models import Session
from guardian.shortcuts import assign_perm
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField

from branches.users.models import Preparer, Staff, Delivery
from branches.models import Branch
from customers.models import Customer
from products.models import Product, Unit
from core.base.models import TimeStampedModel
from users.models import UserAddress


def get_order_number():
    # return random.randint(1000000000, 9999999999)

    with connection.cursor() as cursor:
        cursor.execute("SELECT nextval('order_order_number_seq')")
        result = cursor.fetchone()
        return result[0]


class OrderBlock(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class OrderBlockItem(TimeStampedModel):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    block = models.ForeignKey(
        OrderBlock, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="block_items"
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="block_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product} in {self.block}"


class Cart(TimeStampedModel):
    class Delivery(models.TextChoices):
        FAST = "FAST", _("Fast")
        SCHEDULE = "SCHEDULE", _("Scheduled")

    class Status(models.TextChoices):
        OPEN = "OPEN", _("Open")
        CLOSED = "CLOSED", _("Closed")
        ORDERED = "ORDERED", _("Ordered")
        CANCELED = "CANCELED", _("Canceled")
        ABANDONED = "ABANDONED", _("Abandoned")

    class TypeOfPayment(models.TextChoices):
        CASH = "CASH", _("Cash")
        CARD = "CARD", _("Card")
        ON_DELIVERY = "ON_DELIVERY", _("On Delivery")
        OTHER = "OTHER", _("Other")

    status = models.CharField(
        choices=Status.choices, default=Status.OPEN, max_length=50
    )
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="carts", null=True, blank=True
    )
    anonymous = models.ForeignKey(
        "customers.AnonymousCustomer",
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True,
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True, blank=True
    )
    browsing_key = models.ForeignKey(
        "customers.BrowsingKey",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carts",
    )
    phone_number = PhoneNumberField(null=True, blank=True)
    delivery_type = models.CharField(
        max_length=50, choices=Delivery.choices, default=Delivery.FAST
    )
    user_address = models.ForeignKey(
        UserAddress,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
    )
    type_of_payment = models.CharField(
        max_length=50, choices=TypeOfPayment.choices, default=TypeOfPayment.CASH
    )
    location = models.PointField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    promotion_applied = models.BooleanField(default=False)
    real_price = MoneyField(
        max_digits=10, decimal_places=2, default_currency="SAR", null=True, blank=True
    )
    final_price = MoneyField(
        max_digits=10, decimal_places=2, default_currency="SAR", null=True, blank=True
    )
    discount_amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency="SAR", null=True, blank=True
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    margin_profit = MoneyField(
        max_digits=10, decimal_places=2, default_currency="SAR", null=True, blank=True
    )

    @property
    def address(self):
        if hasattr(self.browsing_key, "address"):
            return self.browsing_key.address

    def save(self, *args, **kwargs):
        # Ensure only one open cart per customer
        if self.status == self.Status.OPEN:
            Cart.objects.filter(customer=self.customer, status=self.Status.OPEN).update(
                status=self.Status.CLOSED
            )

        super().save(*args, **kwargs)

    def mark_as_open(self):
        # Close all other carts for this customer and mark this one as open
        Cart.objects.filter(customer=self.customer, status=self.Status.OPEN).update(
            status=self.Status.CLOSED
        )
        self.status = self.Status.OPEN
        self.save()

    def mark_as_canceled(self):
        # Mark the cart as canceled without deleting it
        self.status = self.Status.CANCELED
        self.save()

    def is_open(self):
        return self.status == self.Status.OPEN


class CartPromotion(TimeStampedModel):
    uid = models.UUIDField(unique=True, editable=True, default=uuid.uuid4)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="promotions")
    applied = models.BooleanField(default=False)
    type = models.CharField(max_length=50, null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    source = GenericForeignKey("content_type", "object_id")


class CartItem(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="SAR")

    price_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="card_items_prices",
    )
    price_id = models.BigIntegerField(null=True, blank=True)
    price_source = GenericForeignKey("price_type", "price_id")

    offer_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cart_items_offers",
    )
    offer_id = models.BigIntegerField(null=True, blank=True)
    offer_source = GenericForeignKey("offer_type", "offer_id")

    offer_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )


class Order(TimeStampedModel):
    class OrderStatus(models.TextChoices):
        PAID = "PAID", _("Paid")
        PENDING = "PENDING", _("Pending Payment")
        PREPARING = "PREPARING", _("Preparing")
        PREPARED = "PREPARED", _("Prepared")
        SHIPPED = "SHIPPED", _("Shipped")
        RECEIVED = "RECEIVED", _("Received")
        CHECKING = "CHECKING", _("Checking")
        CHECKED = "CHECKED", _("Checked")
        DELIVERING = "DELIVERING", _("Delivering")
        DELIVERED = "DELIVERED", _("Delivered")
        DONE = "DONE", _("Done")
        RETURNED = "RETURNED", _("Returned")
        CANCELED = "CANCELED", _("Canceled")
        TRANSFERRED = "TRANSFERRED", _("Transferred")

    id = models.BigAutoField(primary_key=True, editable=False)
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    number = models.PositiveBigIntegerField(
        unique=True, editable=False, default=get_order_number
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    delivery_type = models.CharField(
        max_length=20, choices=Cart.Delivery.choices, default=Cart.Delivery.FAST
    )
    preparation_cost = MoneyField(
        max_digits=10, decimal_places=2, default_currency="SAR", null=True, blank=True
    )
    delivery_cost = MoneyField(
        max_digits=10, decimal_places=2, default_currency="SAR", null=True, blank=True
    )
    total_price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="SAR", null=True, blank=True
    )
    converted_from = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, related_name="converted_orders"
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="orders")
    preparer = models.ForeignKey(
        Preparer,
        on_delete=models.CASCADE,
        related_name="preparation_orders",
        blank=True,
        null=True,
    )
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name="delivery_orders",
        blank=True,
        null=True,
    )
    cashier = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="cashier_orders",
        blank=True,
        null=True,
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders", blank=True, null=True
    )
    phone_number = PhoneNumberField(null=True, blank=True)
    customer_address = models.ForeignKey(
        UserAddress,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="orders",
    )
    location = models.PointField(null=True, blank=True)

    total_order_cost = MoneyField(
        max_digits=10, decimal_places=2, default_currency="SAR", null=True, blank=True
    )
    profit_margin = MoneyField(
        max_digits=10, decimal_places=2, default_currency="SAR", null=True, blank=True
    )

    estimated_delivery_time = models.DurationField(null=True, blank=True)
    estimated_preparing_time = models.DurationField(null=True, blank=True)

    # Time fields for tracking order process
    ordered_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    accepted_preparer_at = models.DateTimeField(null=True, blank=True)
    completed_preparer_at = models.DateTimeField(null=True, blank=True)
    accept_cashier_at = models.DateTimeField(null=True, blank=True)
    complete_cashier_at = models.DateTimeField(null=True, blank=True)
    accepted_delivery_at = models.DateTimeField(null=True, blank=True)
    arrived_delivery_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    # Delayed
    delayed = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Order {self.id}"

    # Centralized method for updating order status and timestamps
    def update_status(self, new_status, timestamp_field=None):
        self.status = new_status
        if timestamp_field:
            setattr(self, timestamp_field, timezone.now())
        self.save()

    def mark_as_paid(self):
        self.update_status(self.OrderStatus.PAID, "paid_at")

    def mark_as_checking(self):
        self.update_status(self.OrderStatus.CHECKING, "accept_cashier_at")

    def mark_as_checked(self):
        self.update_status(self.OrderStatus.CHECKED, "complete_cashier_at")

    def mark_as_preparing(self):
        self.update_status(self.OrderStatus.PREPARING, "accepted_preparer_at")

    def mark_preparation_completed(self):
        self.update_status(self.OrderStatus.PREPARED, "completed_preparer_at")

    def mark_accepted_delivery(self):
        self.update_status(self.OrderStatus.DELIVERING, "accepted_delivery_at")

    def mark_delivery_arrived(self):
        self.update_status(self.OrderStatus.DELIVERED, "arrived_delivery_at")

    def mark_as_delivered(self):
        self.update_status(self.OrderStatus.DELIVERED, "delivered_at")

    # Calculating times between events using properties
    @property
    def waiting_prepare_time(self):
        if (
            self.cart.type_of_payment == "ON_DELIVERY"
            and self.accepted_preparer_at
            and self.accepted_delivery_at
        ):
            return self.accepted_delivery_at - self.accepted_preparer_at
        elif (
            self.cart.type_of_payment == "CARD"
            and self.accepted_preparer_at
            and self.paid_at
        ):
            return self.accepted_preparer_at - self.paid_at
        return None

    @property
    def preparation_duration(self):
        if self.accepted_preparer_at and self.completed_preparer_at:
            return self.completed_preparer_at - self.accepted_preparer_at
        return None

    @property
    def waiting_cashier_time(self):
        if self.completed_preparer_at and self.accept_cashier_at:
            return self.accept_cashier_at - self.completed_preparer_at
        return None

    @property
    def checking_duration(self):
        if self.accept_cashier_at and self.complete_cashier_at:
            return self.complete_cashier_at - self.accept_cashier_at
        return None

    @property
    def waiting_delivery_time(self):
        if self.complete_cashier_at and self.accepted_delivery_at:
            return self.accepted_delivery_at - self.complete_cashier_at
        return None

    @property
    def delivery_duration(self):
        if self.accepted_delivery_at and self.arrived_delivery_at:
            return self.arrived_delivery_at - self.accepted_delivery_at
        return None

    @property
    def time_to_customer(self):
        if self.accepted_delivery_at and self.delivered_at:
            return self.delivered_at - self.accepted_delivery_at
        return None

    @property
    def total_order_time(self):
        if self.ordered_at and self.delivered_at:
            return self.delivered_at - self.ordered_at
        return None

    @property
    def payment_duration(self):
        if self.ordered_at and self.paid_at:
            return self.paid_at - self.ordered_at
        return None
