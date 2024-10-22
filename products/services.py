from products.models import Group, Supplier, Category, Product, Unit, PricingGroup, Barcode, ProductPrice, ProductCost


class GroupService:
    @staticmethod
    def get_all_groups():
        return Group.objects.all()

    @staticmethod
    def get_all_main_groups():
        return Group.objects.filter(parent__isnull=True)

    @staticmethod
    def get_all_sub_groups():
        return Group.objects.filter(parent__isnull=False)

    @staticmethod
    def get_sub_groups_for_main_group(main_group_id):
        return Group.objects.filter(parent__isnull=False, parent__id=main_group_id)





class SupplierService:
    @staticmethod
    def get_all_suppliers():
        return Supplier.objects.all()


class CategoryService:
    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class ProductService:
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.get(pk=product_id)

    @staticmethod
    def get_product_by_name(name):
        return Product.objects.get(name=name)


class UnitService:
    @staticmethod
    def get_all_units():
        return Unit.objects.all()


class PricingGroupService:
    @staticmethod
    def get_all_pricing_groups():
        return PricingGroup.objects.all()


class BarcodeService:
    @staticmethod
    def get_all_barcodes():
        return Barcode.objects.all()


class ProductPriceService:
    @staticmethod
    def get_all_product_prices():
        return ProductPrice.objects.all()


class ProductCostService:
    @staticmethod
    def get_all_product_costs():
        return ProductCost.objects.all()
