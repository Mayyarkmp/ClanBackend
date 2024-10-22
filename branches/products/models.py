import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.constraints import UniqueConstraint
from django.db.models.query import Q
from djmoney.models.fields import MoneyField

from branches.models import Branch
from branches.users.models import BranchUser, Preparer
from core.base.models import TimeStampedModel
from products.models import ProductUnit, Supplier
from users.models import User


class PricingGroup(TimeStampedModel):
    uid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        verbose_name=_("UID"),
    )
    number = models.CharField(max_length=50, unique=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="pricing_groups",
        verbose_name=_("Branch"),
    )
    name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Name")
    )
    name_en = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("English Name")
    )

    codename = models.SlugField(max_length=50, unique=True, verbose_name=_("Codename"))

    def __str__(self):
        return str(self.codename)


class Product(TimeStampedModel):
    class Types(models.TextChoices):
        PRIMARY = "PRIMARY", _("Primary")
        SECONDARY = "SECONDARY", _("Secondary")
        NONE = "NONE", _("None")

    class Status(models.TextChoices):
        ACTIVE = "Active", _("Active")
        INACTIVE = "Inactive", _("Inactive")

    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    number = models.CharField(max_length=50, db_index=True)
    serial_number = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        verbose_name=_("Serial Number"),
    )
    product = models.ForeignKey(
        ProductUnit,
        on_delete=models.CASCADE,
        related_name="branches",
        verbose_name=_("Product"),
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Branch"),
    )
    type = models.CharField(
        _("Product Type"), max_length=20, choices=Types.choices, default=Types.NONE
    )
    status = models.CharField(
        _("Product Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    features = models.ManyToManyField(
        "products.ProductFeature",
        verbose_name=_("Features"),
        related_name="brance_products",
        blank=True,
    )
    supplier = models.ForeignKey(
        Supplier,
        verbose_name=_("Supplier"),
        on_delete=models.CASCADE,
        related_name="branches_products",
        null=True,
        blank=True,
    )

    cost = MoneyField(
        verbose_name=_("Cost"),
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        default=10.00,
    )
    price_net = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        null=True,
        blank=True,
        verbose_name=_("Original Price"),
    )
    
    price_gross = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        null=True,
        blank=True,
        verbose_name=_("Original Price"),
    )
    price = MoneyField(
        verbose_name=_("Price"),
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        default=10.00,
    )
    original_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        null=True,
        blank=True,
        verbose_name=_("Original Price"),
    )

    quantity = models.PositiveIntegerField(_("Quantity"), default=0)

    def save(self, *args, **kwargs):
        if self.number is None:  # التأكد من عدم وجود `null`
            last_number = Product.objects.order_by('-number').first()
            self.number = (last_number.number + 1) if last_number else 1
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["branch", "product"],
                name="unique_product",
                condition=Q(is_deleted=False),
            ),
        ]


class PrimaryShelf(TimeStampedModel):
    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    codename = models.SlugField(_("Codename"), max_length=50, unique=True)
    index = models.PositiveIntegerField(_("Index"), unique=True, db_index=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="shelves",
        verbose_name=_("Branch"),
    )
    name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Name")
    )
    name_en = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("English Name")
    )
    supervisor = models.ForeignKey(
        BranchUser,
        on_delete=models.CASCADE,
        related_name="primary_shelves",
        null=True,
        blank=True,
        verbose_name=_("Supervisor"),
    )

    @property
    def supervisors(self):
        supervisors = set()
        for sub_shelf in getattr(getattr(self, "sub_shelves"), "all"):
            if sub_shelf.supervisors.count() > 0:
                supervisors.update(sub_shelf.supervisors)
        return list(supervisors)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["index", "branch"],
                name="unique_primary_shelf",
                condition=Q(is_deleted=False),
            ),
        ]


class SubShelf(TimeStampedModel):
    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    codename = models.SlugField(_("Codename"), max_length=50, unique=True)
    index = models.PositiveIntegerField(_("Index"), db_index=True)
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    name_en = models.CharField(_("English Name"), max_length=50, blank=True, null=True)
    primary_shelf = models.ForeignKey(
        PrimaryShelf,
        on_delete=models.CASCADE,
        related_name="sub_shelves",
        verbose_name=_("Primary Shelf"),
    )
    supervisor = models.ForeignKey(
        BranchUser,
        related_name="sub_shelves",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Supervisor"),
    )

    @property
    def branch(self):
        return getattr(self.primary_shelf, "branch")

    @property
    def supervisors(self):
        supervisors = []
        for shelf in getattr(getattr(self, "shelves", "all")):
            if shelf.supervisor:
                supervisors.append(shelf.supervisor)
        return supervisors

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["index", "primary_shelf"],
                name="unique_sub_shelf",
                condition=Q(is_deleted=False),
            ),
        ]


class Shelf(TimeStampedModel):
    uid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        verbose_name=_("UID"),
    )
    codename = models.SlugField(max_length=50, unique=True, verbose_name=_("Codename"))
    index = models.PositiveIntegerField(db_index=True, verbose_name=_("Index"))
    sub_shelf = models.ForeignKey(
        SubShelf,
        on_delete=models.CASCADE,
        related_name="shelves",
        verbose_name=_("Sub Shelf"),
    )
    name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Name")
    )
    name_en = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("English Name")
    )
    supervisor = models.ForeignKey(
        Preparer,
        related_name="shelves",
        on_delete=models.CASCADE,
        verbose_name=_("Supervisor"),
    )
    products = models.ManyToManyField(
        Product, related_name="shelves", verbose_name=_("Products")
    )

    @property
    def branch(self):
        return getattr(self.sub_shelf, "branch")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["index", "sub_shelf"],
                name="unique_shelf",
                condition=Q(is_deleted=False),
            ),
        ]


class ProductQuantity(TimeStampedModel):
    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="quantities",
        verbose_name=_("Product"),
    )
    quantity = models.PositiveIntegerField(_("Quantity"))

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class ProductPrice(TimeStampedModel):
    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="prices",
    )

    pricing_group = models.ForeignKey(
        PricingGroup,
        verbose_name=_("Pricing Group"),
        on_delete=models.CASCADE,
        related_name="prices",
    )

    price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="SAR", verbose_name=_("Price")
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["product", "pricing_group"],
                name="unique_product_price",
                condition=Q(is_deleted=False),
            ),
        ]


class ProductChangeStateRequest(TimeStampedModel):
    """
    When Staff request transfer shelf to another shelf
    """

    class RequestTypes(models.TextChoices):
        ACTIVATE = "ACTIVATE", _("Activate")
        DEACTIVATE = "DEACTIVATE", _("Deactivate")

    class Status(models.TextChoices):
        ACCEPTED = "ACCEPTED", _("Accepted")
        REVIEWING = "REVIEWING", _("Reviewing")
        REJECTED = "REJECTED", _("Rejected")

    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    request_type = models.CharField(
        max_length=30, choices=RequestTypes.choices, verbose_name=_("Request Type")
    )
    status = models.CharField(
        default=Status.REVIEWING,
        max_length=20,
        choices=Status.choices,
        verbose_name=_("Status"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="change_state_requests",
        verbose_name=_("Product"),
    )
    creator = models.ForeignKey(
        BranchUser,
        on_delete=models.CASCADE,
        related_name="change_state_requests",
        verbose_name=_("Creator"),
    )


class ProductTransferRequest(TimeStampedModel):
    class Status(models.TextChoices):
        ACCEPTED = "Accepted", _("Accepted")
        REVIEWING = "Reviewing", _("Reviewing")
        REJECTED = "Rejected", _("Rejected")

    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    creator = models.ForeignKey(
        BranchUser,
        on_delete=models.CASCADE,
        related_name="transfer_requests",
        verbose_name=_("Creator"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="transfer_requests",
        verbose_name=_("Products"),
    )
    from_shelf = models.ForeignKey(
        Shelf,
        on_delete=models.CASCADE,
        related_name="transfer_requests",
        verbose_name=_("From Shelf"),
    )
    to_shelf = models.ForeignKey(
        Shelf,
        on_delete=models.CASCADE,
        related_name="receive_requests",
        verbose_name=_("To Shelf"),
    )
    status = models.CharField(
        default=Status.REVIEWING,
        max_length=20,
        choices=Status.choices,
        verbose_name=_("Status"),
    )


class ProductSupplyRequest(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "Pending", _("Pending")
        IN_PROGRESS = "In Progress", _("In Progress")
        COMPLETED = "Completed", _("Completed")
        REJECTED = "Rejected", _("Rejected")
        CANCELLED = "Cancelled", _("Cancelled")
        IN_TRANSIT = "In Transit", _("In Transit")
        ON_HOLD = "On Hold", _("On Hold")
        SUPPLIED = "Supplied", _("Supplied")

    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    status = models.CharField(
        default=Status.PENDING,
        max_length=20,
        choices=Status.choices,
        verbose_name=_("Status"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="supply_requests",
        verbose_name=_("Products"),
    )
    creator = models.ForeignKey(
        BranchUser,
        on_delete=models.CASCADE,
        related_name="created_supply_requests",
        verbose_name=_("Creator"),
    )
    supplier = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="supplied_supply_requests",
        verbose_name=_("Supplier"),
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="supervised_supply_request",
        verbose_name=_("Staff"),
    )


class ProductSupplyAction(TimeStampedModel):
    class Actions(models.TextChoices):
        CREATED = "Created", _("Created")
        UPDATED = "Updated", _("Updated")
        APPROVED = "Approved", _("Approved")
        REJECTED = "Rejected", _("Rejected")
        SUPPLIED = "Supplied", _("Supplied")
        CANCELLED = "Cancelled", _("Cancelled")
        IN_PROGRESS = "In Progress", _("In Progress")
        IN_TRANSIT = "In Transit", _("In Transit")

    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, verbose_name=_("UID")
    )
    action = models.CharField(
        max_length=30, choices=Actions.choices, verbose_name=_("Action")
    )
    request = models.ForeignKey(
        ProductSupplyRequest,
        on_delete=models.CASCADE,
        related_name="actions",
        verbose_name=_("Request"),
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="actions_in_supply_requests",
        verbose_name=_("Actor"),
    )
