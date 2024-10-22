from django.urls import path
from rest_framework_nested import routers
from core.base.routers import register_model_routes
from . import views

app_name = "products"

router = routers.DefaultRouter()
group_router = register_model_routes(
    router,
    "groups",
    views.MainGroupViewSet,
    {
        "sub-groups": (
            views.SubGroupViewSet,
            {
                "products": views.ProductViewSet,
                "brands": (
                    views.BrandViewSet,
                    {
                        "products": views.ProductViewSet,
                        "categories": (
                            views.CategoryViewSet,
                            {
                                "products": views.ProductViewSet,
                                "sub-categories": (
                                    views.CategoryViewSet,
                                    {"products": views.ProductViewSet},
                                    "sub_category",
                                ),
                            },
                            "category",
                        ),
                    },
                    "brand",
                ),
            },
            "sub_group",
        ),
        "products": views.ProductViewSet,
    },
    "group",
)

# Main Groups Router
main_group_router = register_model_routes(
    router,
    "main-groups",
    views.MainGroupViewSet,
    {
        "sub-groups": (
            views.SubGroupViewSet,
            {
                "products": views.ProductViewSet,
                "brands": (
                    views.BrandViewSet,
                    {
                        "products": views.ProductViewSet,
                        "categories": (
                            views.CategoryViewSet,
                            {
                                "products": views.ProductViewSet,
                                "sub-categories": (
                                    views.CategoryViewSet,
                                    {"products": views.ProductViewSet},
                                    "sub_category",
                                ),
                            },
                            "category",
                        ),
                    },
                    "brand",
                ),
            },
            "sub_group",
        ),
        "products": views.ProductViewSet,
    },
    "main_group",
)

# Sub Groups Router
sub_group_router = register_model_routes(
    router,
    "sub-groups",
    views.SubGroupViewSet,
    {
        "products": views.ProductViewSet,
        "brands": (
            views.BrandViewSet,
            {
                "products": views.ProductViewSet,
                "categories": (
                    views.CategoryViewSet,
                    {
                        "products": views.ProductViewSet,
                        "sub-categories": (
                            views.CategoryViewSet,
                            {"products": views.ProductViewSet},
                            "sub_category",
                        ),
                    },
                    "category",
                ),
            },
            "brand",
        ),
        "categories": (
            views.CategoryViewSet,
            {
                "products": views.ProductViewSet,
                "sub-categories": (
                    views.CategoryViewSet,
                    {"products": views.ProductViewSet},
                    "sub_category",
                ),
                "brands": (
                    views.BrandViewSet,
                    {"products": views.ProductViewSet},
                    "brand",
                ),
            },
            "category",
        ),
        "packs": (views.PackViewSet, {"products": views.ProductViewSet}, "pack"),
    },
    "sub_group",
)

# Categories Router
category_router = register_model_routes(
    router,
    "categories",
    views.CategoryViewSet,
    {
        "products": views.ProductViewSet,
        "sub-categories": (
            views.CategoryViewSet,
            {
                "products": views.ProductViewSet,
                "brands": (
                    views.BrandViewSet,
                    {"products": views.ProductViewSet},
                    "brand",
                ),
            },
            "sub_category",
        ),
        "brands": (views.BrandViewSet, {"products": views.ProductViewSet}, "brand"),
        "main-groups": (
            views.MainGroupViewSet,
            {
                "sub-groups": (
                    views.SubGroupViewSet,
                    {"products": views.ProductViewSet},
                    "sub_group",
                ),
                "products": views.ProductViewSet,
            },
            "main_group",
        ),
        "sub-groups": (
            views.SubGroupViewSet,
            {"products": views.ProductViewSet},
            "sub_group",
        ),
    },
    "category",
)

# Packs Router
pack_router = register_model_routes(
    router,
    "packs",
    views.PackViewSet,
    {
        "products": views.ProductViewSet,
        "main-groups": (
            views.MainGroupViewSet,
            {
                "sub-groups": (
                    views.SubGroupViewSet,
                    {"products": views.ProductViewSet},
                    "sub_group",
                ),
                "products": views.ProductViewSet,
            },
            "main_group",
        ),
        "sub-groups": (
            views.SubGroupViewSet,
            {"products": views.ProductViewSet},
            "sub_group",
        ),
        "categories": (
            views.CategoryViewSet,
            {
                "products": views.ProductViewSet,
                "sub-categories": (
                    views.CategoryViewSet,
                    {"products": views.ProductViewSet},
                    "sub_category",
                ),
                "brands": (
                    views.BrandViewSet,
                    {"products": views.ProductViewSet},
                    "brand",
                ),
            },
            "category",
        ),
        "brands": (views.BrandViewSet, {"products": views.ProductViewSet}, "brand"),
    },
    "pack",
)

# Brands Router
brand_router = register_model_routes(
    router,
    "brands",
    views.BrandViewSet,
    {
        "products": views.ProductViewSet,
        "categories": (
            views.CategoryViewSet,
            {
                "products": views.ProductViewSet,
                "sub-categories": (
                    views.CategoryViewSet,
                    {"products": views.ProductViewSet},
                    "sub_category",
                ),
            },
            "category",
        ),
        "main-groups": (
            views.MainGroupViewSet,
            {
                "sub-groups": (
                    views.SubGroupViewSet,
                    {"products": views.ProductViewSet},
                    "sub_group",
                ),
                "products": views.ProductViewSet,
            },
            "main_group",
        ),
        "sub-groups": (
            views.SubGroupViewSet,
            {"products": views.ProductViewSet},
            "sub_group",
        ),
    },
    "brand",
)


product_router = register_model_routes(
    router,
    "",
    views.ProductViewSet,
    {
        "sub-group": views.SubGroupViewSet,
        "main-group": views.MainGroupViewSet,
        "categories": views.CategoryViewSet,
        "brands": views.BrandViewSet,
        "packs": views.PackViewSet,
    },
    "product",
)


urlpatterns = []

urlpatterns += router.urls
urlpatterns += group_router.urls
urlpatterns += main_group_router.urls
urlpatterns += sub_group_router.urls
urlpatterns += category_router.urls
urlpatterns += pack_router.urls
urlpatterns += brand_router.urls
