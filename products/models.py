import uuid
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from core.media.models import Media
from core.base.models import TimeStampedModel
from django_measurement.models import MeasurementField
from django.contrib.postgres.fields import ArrayField
from measurement.measures import Weight


class Group(TimeStampedModel):
    """Model for Main Group and Sub Groups for Products"""

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50, db_index=True)
    name = models.CharField(_("Name"), max_length=100, db_index=True)
    name_en = models.CharField(_("English Name"), max_length=100, blank=True, null=True)
    profit_margin = models.IntegerField(
        _("Profit Margin"), default=0, null=True, blank=True
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name=_("Parent Group"),
    )
    images = models.ManyToManyField(
        Media, related_name="groups", blank=True, verbose_name=_("Images")
    )
    default_image = models.CharField(
        _("Default Image"), max_length=255, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.number is None:  # التأكد من عدم وجود `null`
            last_number = Product.objects.order_by('-number').first()
            self.number = (last_number.number + 1) if last_number else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class Supplier(TimeStampedModel):
    """Model for Products Suppliers"""

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50, db_index=True)
    name = models.CharField(_("Name"), max_length=100)
    name_en = models.CharField(_("English Name"), max_length=100, null=True, blank=True)
    images = models.ManyToManyField(
        Media, verbose_name=_("Images"), blank=True, related_name="suppliers"
    )
    default_image = models.CharField(
        _("Default Image"), max_length=255, null=True, blank=True
    )
    categories = models.ManyToManyField(
        "Category", verbose_name=_("Categories"), related_name="suppliers", blank=True
    )
    groups = models.ManyToManyField(
        "Group", verbose_name=_("Groups"), related_name="suppliers", blank=True
    )


    def save(self, *args, **kwargs):
        if self.number is None:  # التأكد من عدم وجود `null`
            last_number = Product.objects.order_by('-number').first()
            self.number = (last_number.number + 1) if last_number else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")


class Brand(TimeStampedModel):
    """Model for Product Brands"""

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50, db_index=True)
    name = models.CharField(_("Name"), max_length=255)
    name_en = models.CharField(_("English Name"), max_length=255, null=True, blank=True)
    images = models.ManyToManyField(
        Media,
        blank=True,
        verbose_name=_("Images"),
        related_name="brands",
    )
    default_image = models.CharField(_("Default Image"), blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.number is None:  # التأكد من عدم وجود `null`
            last_number = Product.objects.order_by('-number').first()
            self.number = (last_number.number + 1) if last_number else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")


class Category(TimeStampedModel):
    """Model for Product Categories"""

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50, db_index=True)
    name = models.CharField(_("Name"), max_length=100)
    name_en = models.CharField(_("English Name"), max_length=100, blank=True, null=True)
    images = models.ManyToManyField(
        Media,
        blank=True,
        verbose_name=_("Images"),
        related_name="categories",
    )
    default_image = models.CharField(_("Default Image"), blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name=_("Main Category"),
        on_delete=models.SET_NULL,
        related_name="children",
    )


    def save(self, *args, **kwargs):
        if self.number is None:  # التأكد من عدم وجود `null`
            last_number = Product.objects.order_by('-number').first()
            self.number = (last_number.number + 1) if last_number else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Unit(TimeStampedModel):
    """Model for Product Units"""

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50, db_index=True)
    name = models.CharField(_("Name"), max_length=100, db_index=True)
    name_en = models.CharField(_("English Name"), max_length=100, blank=True, null=True)
    codename = models.SlugField(
        max_length=50, unique=True, db_index=True, verbose_name=_("Codename")
    )
    factor_unit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Factor Unit"),
        related_name="subunits",
    )
    conversion_factor = models.DecimalField(
        _("Conversion factor"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_factor = models.BooleanField(_("Is Factor"), default=False)


    def save(self, *args, **kwargs):
        if self.number is None:  # التأكد من عدم وجود `null`
            last_number = Product.objects.order_by('-number').first()
            self.number = (last_number.number + 1) if last_number else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")


class Product(TimeStampedModel):
    """Model for Products"""

    class Types(models.TextChoices):
        PRIMARY = "PRIMARY", _("Primary")
        SECONDARY = "SECONDARY", _("Secondary")
        NONE = "None", _("None")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=100, db_index=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    name_en = models.CharField(_("English Name"), max_length=100, blank=True, null=True)
    description_en = models.TextField(_("English Description"), blank=True, null=True)
    sq = models.CharField(
        max_length=255, db_index=True, unique=True, verbose_name=_("SQ")
    )

    type = models.CharField(
        max_length=255,
        choices=Types.choices,
        default=Types.NONE,
        verbose_name=_("Type"),
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    features = models.ManyToManyField(
        "ProductFeature",
        verbose_name=_("Features"),
        related_name="products",
        blank=True,
    )

    serial_number = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        verbose_name=_("Serial Number"),
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Group"),
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
        verbose_name=_("Brand"),
    )
    categories = models.ManyToManyField(
        Category, verbose_name=_("Category"), related_name="products", blank=True
    )

    supplier = models.ForeignKey(
        Supplier,
        verbose_name=_("Supplier"),
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    images = models.ManyToManyField(
        Media,
        blank=True,
        verbose_name=_("Images"),
        related_name="products",
    )
    default_image = models.CharField(_("Default Image"), blank=True, null=True)
    profit_margin = models.DecimalField(
        _("Profit Margin"), decimal_places=2, max_digits=10, null=True, blank=True
    )


    def __str__(self):
        return f"{self.name}"

    @property
    def main_group(self):
        """Get Main Group For Product"""
        if hasattr(self.group, "parent"):
            return getattr(self.group, "parent")
        return None

    @property
    def sub_group(self):
        """Get Sub Group For Product"""
        return self.group

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductUnit(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50, db_index=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, to_field="sq", related_name="units"
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="products")
    cost = MoneyField(
        verbose_name=_("Cost"),
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        null=True,
        blank=True,
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
        null=True,
        blank=True,
    )
    original_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        null=True,
        blank=True,
        verbose_name=_("Original Price"),
    )
    serial_number = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Serial Number"),
    )
    weight = MeasurementField(
        measurement=Weight,
        unit_choices=[("g", "g"), ("kg", "kg")],
        null=True,
        blank=True,
        verbose_name=_("Weight"),
    )
    barcodes = ArrayField(
        models.CharField(max_length=255, db_index=True, verbose_name=_("Barcode")),
        verbose_name=_("Barcodes"),
        null=True,
        blank=True,
    )
    profit_margin = models.DecimalField(
        _("Profit Margin"), decimal_places=2, max_digits=10, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    images = models.ManyToManyField(
        Media, verbose_name=_("Images"), blank=True, related_name="products_units"
    )
    default_image = models.CharField(
        _("Default Image"), max_length=255, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "unit"],
                name="unique_product_unit",
                condition=Q(is_deleted=False),
            ),
        ]
        verbose_name = _("Product Unit")
        verbose_name_plural = _("Product Units")


class ProductFeature(models.Model):
    """Model for Product Features"""

    FEATURE_CHOICES = [
        ("active", _("Active")),
        ("featured", _("Featured")),
        ("new", _("New")),
        ("sale", _("Sale")),
        ("bestseller", _("Bestseller")),
        ("trending", _("Trending")),
        ("top_rated", _("Top Rated")),
        ("popular", _("Popular")),
        ("discount", _("Discount")),
        ("bundle", _("Bundle")),
        ("gift", _("Gift")),
        ("limited_edition", _("Limited Edition")),
        ("preorder", _("Preorder")),
        ("subscription", _("Subscription")),
        ("customizable", _("Customizable")),
        ("digital", _("Digital")),
        ("physical", _("Physical")),
        ("service", _("Service")),
        ("virtual", _("Virtual")),
        ("downloadable", _("Downloadable")),
        ("returnable", _("Returnable")),
        ("refundable", _("Refundable")),
        ("shipping_required", _("Shipping Required")),
        ("shipping_free", _("Shipping Free")),
    ]

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Feature"), max_length=50, choices=FEATURE_CHOICES)
    custom_name = models.CharField(
        _("Custom Name"), max_length=100, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name or self.custom_name}"

    class Meta:
        verbose_name = _("Product Feature")
        verbose_name_plural = _("Product Features")


class PricingGroup(TimeStampedModel):
    """Model for Pricing Groups"""

    uid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    number = models.CharField(max_length=50, db_index=True)
    name = models.CharField(_("Name"), max_length=100, db_index=True)
    name_en = models.CharField(_("English Name"), max_length=100, blank=True, null=True)
    codename = models.SlugField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Pricing Group")
        verbose_name_plural = _("Pricing Groups")


class ProductPrice(TimeStampedModel):
    """Model for Product Prices"""

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50, db_index=True)
    product = models.ForeignKey(
        ProductUnit,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="prices",
    )
    pricing_group = models.ForeignKey(
        PricingGroup,
        verbose_name=_("Pricing Group"),
        on_delete=models.CASCADE,
        related_name="products_prices",
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
        verbose_name=_("Price"), max_digits=14, decimal_places=2, default_currency="SAR"
    )

    original_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="SAR",
        null=True,
        blank=True,
        verbose_name=_("Original Price"),
    )

    @property
    def unit(self):
        return getattr(self.product, "unit")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "pricing_group"],
                name="unique_product_pricing_group",
                condition=Q(is_deleted=False),
            )
        ]
        verbose_name = _("Product Price")
        verbose_name_plural = _("Product Prices")
