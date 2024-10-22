"""
    Urls For Stores in Prodject
"""

from rest_framework_nested import routers
from django.urls import include, path
from core.base.routers import register_model_routes
from offers.classification.views import PackViewSet, SubPackViewSet, MainPackViewSet

from .views import (
    GroupViewSet,
    SubGroupViewSet,
    MainGroupViewSet,
    SupplierViewSet,
    UnitViewSet,
    CategoryViewSet,
    PricingGroupViewSet,
    ProductPriceViewSet,
    ProductViewSet,
    ProductUnitViewSet,
    ProductQuantityViewSet,
    ProductPricesViewSet,
    BrandViewSet,
)


app_name = "products"

router = routers.DefaultRouter()

main_group_router = register_model_routes(
    router,
    "groups/main",
    MainGroupViewSet,
    {
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "units": ProductUnitViewSet,
            },
            "product",
        ),
        "sub": (
            SubGroupViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
    
                        "units": ProductUnitViewSet,
                        
                        "quantities": ProductQuantityViewSet,
                    },
                    "product",
                ),
                "categories": (
                    CategoryViewSet,
                    {
                        "products": (
                            ProductViewSet,
                            {
                                "prices": ProductPricesViewSet,
            
                                "units": ProductUnitViewSet,
                                
                            },
                            "product",
                        ),
                    },
                    "category",
                ),
            },
            "sub_group",
        ),
        "categories": (
            CategoryViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
    
                        "units": ProductUnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "category",
        ),
        "suppliers": (
            SupplierViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
    
                        "units": ProductUnitViewSet,
                        
                    },
                    "product",
                ),
                "categories": (
                    CategoryViewSet,
                    {
                        "products": (
                            ProductViewSet,
                            {
                                "prices": ProductPricesViewSet,
            
                                "units": ProductUnitViewSet,
                            },
                            "product",
                        ),
                    },
                    "category",
                ),
            },
            "supplier",
        ),
    },
    "main_group",
)


sub_group_router = register_model_routes(
    router,
    "groups/sub",
    SubGroupViewSet,
    {
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "units": ProductUnitViewSet,
            },
            "product",
        ),
        "categories": (
            CategoryViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "units": ProductUnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "category",
        ),
        "suppliers": (
            SupplierViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "units": ProductUnitViewSet,
                    },
                    "product",
                ),
                "categories": (
                    CategoryViewSet,
                    {
                        "products": (
                            ProductViewSet,
                            {
                                "prices": ProductPricesViewSet,
                                "units": ProductUnitViewSet,
                            },
                            "product",
                        ),
                    },
                    "category",
                ),
            },
            "supplier",
        ),
    },
    "sub_group",
)


supplier_router = register_model_routes(
    router,
    "suppliers",
    SupplierViewSet,
    {
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "units": ProductUnitViewSet,
            },
            "product",
        ),
        "main-groups": (
            MainGroupViewSet,
            {
                "sub-groups": (
                    SubGroupViewSet,
                    {
                        "products": (
                            ProductViewSet,
                            {
                                "prices": ProductPricesViewSet,
            
                                "units": ProductUnitViewSet,
                                
                            },
                            "product",
                        ),
                    },
                    "sub_group",
                ),
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
    
                        "units": ProductUnitViewSet,
                        
                    },
                    "product",
                ),
                "categories": (
                    CategoryViewSet,
                    {
                        "products": (
                            ProductViewSet,
                            {
                                "prices": ProductPricesViewSet,
            
                                "units": ProductUnitViewSet,
                            },
                            "product",
                        ),
                    },
                    "category",
                ),
            },
            "main_group",
        ),
        "groups": (
            GroupViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
    
                        "units": ProductUnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "group",
        ),
        "categories": (
            CategoryViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
    
                        "units": ProductUnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "category",
        ),
        "sub-groups": (
            SubGroupViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
    
                        "units": ProductUnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "sub_group",
        ),
    },
    "supplier",
)

group_router = register_model_routes(
    router,
    "groups",
    GroupViewSet,
    {
        "sub": (
            SubGroupViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "units": ProductUnitViewSet
                    },
                    "product",
                ),
            },
            "sub_group",
        ),
        "suppliers": (
            SupplierViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
    
                        "units": ProductUnitViewSet,
                        
                    },
                    "product",
                ),
                "categories": (
                    CategoryViewSet,
                    {
                        "products": (
                            ProductViewSet,
                            {
                                "prices": ProductPricesViewSet,
            
                                "units": ProductUnitViewSet,
                            },
                            "product",
                        ),
                    },
                    "category",
                ),
            },
            "supplier",
        ),
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "units": ProductUnitViewSet,
                
            },
            "product",
        ),
    },
    "group",
)

category_router = register_model_routes(
    router,
    "categories",
    CategoryViewSet,
    {
        "sub": (
            CategoryViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "unit": ProductUnitViewSet,
                    },
                    "product",
                ),
            },
            "sub_category",
        ),
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "units": ProductUnitViewSet,
            },
            "product",
        ),
        "suppliers": SupplierViewSet,
    },
    "category",
)

product_router = register_model_routes(
    router,
    "products",
    ProductViewSet,
    {
        "group": GroupViewSet,
        "sub-group": SubGroupViewSet,
        "main-group": MainGroupViewSet,
        "categories": CategoryViewSet,
        "supplier": SupplierViewSet,
        "units": ProductUnitViewSet,
        "pricing-groups": PricingGroupViewSet,
        "prices": ProductPriceViewSet,
        "quantities": ProductQuantityViewSet,
    },
    "product",
)

product_unit_router = register_model_routes(
    router,
    "products-units",
    ProductUnitViewSet,
    {
        "product": ProductViewSet,
        "unit": UnitViewSet,
        "pricing-group": PricingGroupViewSet,
        "quantities": ProductQuantityViewSet,
        "prices": ProductPriceViewSet,
        "packs": PackViewSet,
        "sub-packs": SubPackViewSet,
        "main-packs": MainPackViewSet,
        "categories": CategoryViewSet,
        "supplier": SupplierViewSet,
        "group": GroupViewSet,
        "sub-group": SubGroupViewSet,
        "main-group": MainGroupViewSet,
    },
    "product_unit",
)

unit_router = register_model_routes(
    router,
    "units",
    UnitViewSet,
    {
        "products": ProductViewSet,
        "pricing-groups": PricingGroupViewSet,
        "prices": ProductPriceViewSet,
        
    },
    "unit",
)

pricing_group_router = register_model_routes(
    router,
    "pricing-groups",
    PricingGroupViewSet,
    {
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "unit": UnitViewSet,
            },
            "product",
        ),
        "units": UnitViewSet,
    },
    "pricing_group",
)


product_price_router = register_model_routes(
    router,
    "products-prices",
    ProductPriceViewSet,
    {
        "product": ProductViewSet,
        "unit": UnitViewSet,
        "pricing-group": PricingGroupViewSet,
    },
    "product_price",
)


main_pack_router = register_model_routes(
    router,
    "packs/main",
    MainPackViewSet,
    {
        "sub": SubPackViewSet,
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "unit": UnitViewSet,
            },
            "product",
        ),
        "main_groups": MainGroupViewSet,
        "sub_groups": SubGroupViewSet,
        "groups": GroupViewSet,
        "categories": CategoryViewSet,
        "suppliers": SupplierViewSet,
        "brands": BrandViewSet,
    },
    "pack",
)
sub_pack_router = register_model_routes(
    router,
    "packs/sub",
    SubPackViewSet,
    {
        "sub": SubPackViewSet,
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "unit": UnitViewSet,
            },
            "product",
        ),
        "main_groups": MainGroupViewSet,
        "sub_groups": SubGroupViewSet,
        "groups": GroupViewSet,
        "categories": CategoryViewSet,
        "suppliers": SupplierViewSet,
        "brands": BrandViewSet,
    },
    "pack",
)

pack_router = register_model_routes(
    router,
    "packs",
    PackViewSet,
    {
        "sub": SubPackViewSet,
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "unit": UnitViewSet,
            },
            "product",
        ),
        "main_groups": MainGroupViewSet,
        "sub_groups": SubGroupViewSet,
        "groups": GroupViewSet,
        "categories": CategoryViewSet,
        "suppliers": SupplierViewSet,
        "brands": BrandViewSet,
    },
    "pack",
)

brand_router = register_model_routes(
    router,
    "brands",
    BrandViewSet,
    {
        "products": (
            ProductViewSet,
            {
                "prices": ProductPricesViewSet,
                "unit": UnitViewSet,
            },
            "product",
        ),
        "main-groups": (
            MainGroupViewSet,
            {
                "sub-groups": SubGroupViewSet,
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "unit": UnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "main_group",
        ),
        "sub-groups": (
            SubGroupViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "unit": UnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "sub_group",
        ),
        "groups": (
            GroupViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "unit": UnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "group",
        ),
        "categories": (
            CategoryViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "unit": UnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "category",
        ),
        "suppliers": (
            SupplierViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "unit": UnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "supplier",
        ),
        "packs": (
            PackViewSet,
            {
                "products": (
                    ProductViewSet,
                    {
                        "prices": ProductPricesViewSet,
                        "unit": UnitViewSet,
                        
                    },
                    "product",
                ),
            },
            "pack",
        ),
    },
    "brand",
)


urlpatterns = [
    path("branches/", include("branches.products.urls", namespace="products"))
]

urlpatterns += router.urls
urlpatterns += group_router.urls
urlpatterns += main_group_router.urls
urlpatterns += sub_group_router.urls
urlpatterns += supplier_router.urls
urlpatterns += category_router.urls
urlpatterns += product_router.urls
urlpatterns += product_unit_router.urls
urlpatterns += unit_router.urls
urlpatterns += pricing_group_router.urls
urlpatterns += product_price_router.urls
urlpatterns += main_pack_router.urls
urlpatterns += sub_pack_router.urls
urlpatterns += pack_router.urls
urlpatterns += brand_router.urls
