import uuid
from django.utils.translation import gettext_lazy as _
from core.base.models import TimeStampedModel
from django.contrib.gis.db import models

from products.models import Product, Supplier, Category, Group, Brand


class PackProduct(models.Model):
    pack = models.ForeignKey(
        "offers_classification.Pack",
        on_delete=models.CASCADE,
        related_name="pack_products",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="pack_packs"
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        unique_together = (("pack", "product"),)

    def __str__(self):
        return f"{self.product} in {self.pack} (Active: {self.is_active})"


class PackGroup(models.Model):
    pack = models.ForeignKey(
        "offers_classification.Pack",
        on_delete=models.CASCADE,
        related_name="pack_groups",
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="pack_packs"
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        unique_together = (("pack", "group"),)

    def __str__(self):
        return f"{self.group} in {self.pack} (Active: {self.is_active})"


class PackCategory(models.Model):
    pack = models.ForeignKey(
        "offers_classification.Pack",
        on_delete=models.CASCADE,
        related_name="pack_categories",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="pack_packs"
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        unique_together = (("pack", "category"),)

    def __str__(self):
        return f"{self.category} in {self.pack} (Active: {self.is_active})"


class PackSupplier(models.Model):
    pack = models.ForeignKey(
        "offers_classification.Pack",
        on_delete=models.CASCADE,
        related_name="pack_suppliers",
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="pack_packs"
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        unique_together = (("pack", "supplier"),)

    def __str__(self):
        return f"{self.supplier} in {self.pack} (Active: {self.is_active})"


class PackBrand(models.Model):
    pack = models.ForeignKey(
        "offers_classification.Pack",
        on_delete=models.CASCADE,
        related_name="pack_brands",
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="pack_packs"
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        unique_together = (("pack", "brand"),)

    def __str__(self):
        return f"{self.brand} in {self.pack} (Active: {self.is_active})"


class Pack(TimeStampedModel):
    class Per(models.TextChoices):
        GROUP = "GROUP", _("Group")
        CATEGORY = "CATEGORY", _("Category")
        SUPPLIER = "SUPPLIER", _("Supplier")
        PRODUCT = "PRODUCT", _("Product")
        BRAND = "BRAND", _("Brand")
        MIXIN = "MIXIN", _("Mixin")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    per = models.CharField(max_length=10, choices=Per.choices, default=Per.MIXIN)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.ManyToManyField("media.Media", related_name="packs", blank=True)
    default_image = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    description_en = models.TextField(blank=True, null=True)

    products = models.ManyToManyField(
        Product,
        verbose_name=_("Products"),
        related_name="packs",
        blank=True,
        through="PackProduct",
        through_fields=("pack", "product"),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("Groups"),
        related_name="packs",
        blank=True,
        through="PackGroup",
        through_fields=("pack", "group"),
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name=_("Categories"),
        related_name="packs",
        blank=True,
        through="PackCategory",
        through_fields=("pack", "category"),
    )
    suppliers = models.ManyToManyField(
        Supplier,
        verbose_name=_("Suppliers"),
        related_name="packs",
        blank=True,
        through="PackSupplier",
        through_fields=("pack", "supplier"),
    )
    brands = models.ManyToManyField(
        Brand,
        verbose_name=_("Brands"),
        related_name="packs",
        blank=True,
        through="PackBrand",
        through_fields=("pack", "brand"),
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        blank=True,
        null=True,
    )
    is_draft = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_all_products(self):
        direct_products = getattr(self.products, "all")
        group_products = Product.objects.filter(group__in=getattr(self.groups, "all"))
        category_products = Product.objects.filter(
            categories__in=getattr(self.categories, "all")
        )
        supplier_products = Product.objects.filter(
            supplier__in=getattr(self.suppliers, "all")
        )
        all_products = Product.objects.none()
        all_products = all_products.union(
            direct_products, group_products, category_products, supplier_products
        ).distinct()

        return all_products

    def get_active_products(self):
        group_products = Product.objects.filter(group__in=getattr(self.groups, "all"))
        category_products = Product.objects.filter(
            categories__in=getattr(self.categories, "all")
        )
        supplier_products = Product.objects.filter(
            supplier__in=getattr(self.suppliers, "all")
        )
        all_products = Product.objects.none()
        all_products = all_products.union(
            getattr(self.products, "all"),
            group_products,
            category_products,
            supplier_products,
        ).distinct()
        deactivated_groups = PackGroup.objects.filter(
            pack=self, is_active=False
        ).values_list("group", flat=True)
        all_products = all_products.exclude(group__in=deactivated_groups)
        deactivated_categories = PackCategory.objects.filter(
            pack=self, is_active=False
        ).values_list("category", flat=True)
        all_products = all_products.exclude(categories__in=deactivated_categories)
        deactivated_suppliers = PackSupplier.objects.filter(
            pack=self, is_active=False
        ).values_list("supplier", flat=True)
        all_products = all_products.exclude(supplier__in=deactivated_suppliers)
        deactivated_products = PackProduct.objects.filter(
            pack=self, is_active=False
        ).values_list("product", flat=True)
        active_products = all_products.exclude(id__in=deactivated_products)

        return active_products

    def get_deactivated_products(self):
        deactivated_product_ids = PackProduct.objects.filter(
            offer=self, is_active=False
        ).values_list("product_id", flat=True)
        deactivated_products = Product.objects.filter(id__in=deactivated_product_ids)

        deactivated_group_ids = PackGroup.objects.filter(
            offer=self, is_active=False
        ).values_list("group_id", flat=True)
        products_from_deactivated_groups = Product.objects.filter(
            group__in=deactivated_group_ids
        )

        deactivated_category_ids = PackCategory.objects.filter(
            offer=self, is_active=False
        ).values_list("category_id", flat=True)
        products_from_deactivated_categories = Product.objects.filter(
            categories__in=deactivated_category_ids
        )

        deactivated_supplier_ids = PackSupplier.objects.filter(
            offer=self, is_active=False
        ).values_list("supplier_id", flat=True)
        products_from_deactivated_suppliers = Product.objects.filter(
            supplier__in=deactivated_supplier_ids
        )
        
        deactivated_brand_ids = PackBrand.objects.filter(
            offer=self, is_active=False
        ).values_list("brand_id", flat=True)
        products_from_deactivated_brands = Product.objects.filter(
            brand__in=deactivated_brand_ids
        )

        deactivated_products = deactivated_products.union(
            products_from_deactivated_groups,
            products_from_deactivated_categories,
            products_from_deactivated_suppliers,
            products_from_deactivated_brands
        ).distinct()

        return deactivated_products
