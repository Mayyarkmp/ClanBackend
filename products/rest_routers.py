


# from rest_framework_nested import routers
# from .views import (
#     GroupViewSet,
#     SupplierViewSet,
#     UnitViewSet,
#     BarcodeViewSet,
#     CategoryViewSet,
#     ProductCostViewSet,
#     PricingGroupViewSet,
#     ProductPriceViewSet,
#     ProductViewSet,
#     GroupProductViewSet, SubGroupViewSet, MainGroupViewSet
# )
#

#
# router = routers.DefaultRouter()
# router.register(r'groups/main', MainGroupViewSet, basename="main-group")
# router.register(r'groups/sub', SubGroupViewSet, basename="sub-group")
# router.register(r'groups', GroupViewSet, basename='group')
# router.register(r'suppliers', SupplierViewSet, basename='supplier')
# router.register(r'units', UnitViewSet, basename='unit')
# router.register(r'barcodes', BarcodeViewSet, basename='barcode')
# router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'pricing-groups', PricingGroupViewSet, basename='pricing-group')
# router.register(r'products', ProductViewSet, basename='product')
# router.register(r'products-costs', ProductCostViewSet, basename='product-cost')
# router.register(r'products-prices', ProductPriceViewSet, basename='product-price')
#
# # Nested routers for group
# group_router = routers.NestedSimpleRouter(router, r'groups', lookup='group')
# group_router.register(r'sub', SubGroupViewSet, basename='group-sub-groups')
#
# group_router.register(r'suppliers', SupplierViewSet, basename='group-suppliers')
# group_router.register(r'products', ProductViewSet, basename='group-products')
# main_group_router = routers.NestedSimpleRouter(router, r'groups/main', lookup='group')
# main_group_router.register(r'sub', SubGroupViewSet, basename='main-group-sub-groups')
# main_group_router.register(r'suppliers', SupplierViewSet, basename='main-group-suppliers')
# main_group_router.register(r'products', ProductViewSet, basename='main-group-products')
# sub_group_router = routers.NestedSimpleRouter(router, r'groups/sub', lookup='group')
# sub_group_router.register(r'suppliers', SupplierViewSet, basename='sub-group-suppliers')
# sub_group_router.register(r'products', ProductViewSet, basename='sub-group-products')
# # Nested routers for category
# category_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
# category_router.register(r'sub-categories', CategoryViewSet, basename='category-sub-categories')
# category_router.register(r'products', ProductViewSet, basename='category-products')
#
# # Nested routers for supplier
# supplier_router = routers.NestedSimpleRouter(router, r'suppliers', lookup='supplier')
# supplier_router.register(r'groups', GroupViewSet, basename='supplier-groups')
# supplier_router.register(r'categories', CategoryViewSet, basename='supplier-categories')
# supplier_router.register(r'products', ProductViewSet, basename='supplier-products')
#
# # Nested routers for unit
# unit_router = routers.NestedSimpleRouter(router, r'units', lookup='unit')
# unit_router.register(r'factor-unit', UnitViewSet, basename='unit-factor-unit')
# unit_router.register(r'units', UnitViewSet, basename='unit-units')
# unit_router.register(r'products', ProductViewSet, basename='unit-products')
#
# # Nested routers for product
# product_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
# product_router.register(r'group', GroupProductViewSet, basename='product-group')
# product_router.register(r'categories', CategoryViewSet, basename='product-categories')
# product_router.register(r'suppliers', SupplierViewSet, basename='product-suppliers')
# product_router.register(r'units', UnitViewSet, basename='product-units')
# product_router.register(r'barcodes', BarcodeViewSet, basename='product-barcodes')
# product_router.register(r'pricing-groups', PricingGroupViewSet, basename='product-pricing-groups')
# product_router.register(r'costs', ProductCostViewSet, basename='product-costs')
# product_router.register(r'prices', ProductPriceViewSet, basename='product-prices')
#
# # Aggregate URLs
# urlpatterns = router.urls
# urlpatterns += supplier_router.urls
# urlpatterns += product_router.urls
# urlpatterns += unit_router.urls
# urlpatterns += category_router.urls
# urlpatterns += group_router.urls
# urlpatterns += main_group_router.urls
# urlpatterns += sub_group_router.urls
from django.urls import include, path

from .rest_routers import urlpatterns as rest_routers

urlpatterns = []
urlpatterns += rest_routers
# urlpatterns += auto_routers