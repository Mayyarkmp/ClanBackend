from rest_framework_nested import routers
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField, ManyToManyRel, ManyToOneRel
from django.utils.text import slugify

class Router:
    def __init__(self, urlpatterns):
        self.urls = urlpatterns

    def add(self, urlpatterns, *args, **kwargs):
        if isinstance(urlpatterns, (list, tuple)):
            self.urls += urlpatterns





# def register_model_routes(router, prefix, viewset, related_viewsets=None, lookup=None):
#     router.register(prefix, viewset, basename=prefix)
#
#     if related_viewsets:
#         lookup = lookup or prefix
#         parent_router = routers.NestedSimpleRouter(router, prefix, lookup=lookup)
#         for related_prefix, related_viewset in related_viewsets.items():
#             parent_router.register(related_prefix, related_viewset, basename=f'{prefix}-{related_prefix}')
#
#         return parent_router
#
#     return None

def register_model_routes(router, prefix, viewset, related_viewsets=None, lookup=None):
    """
    Register a model route with support for nested routers and custom lookup fields.
    :param router: The base router to register with.
    :param prefix: The prefix of the route.
    :param viewset: The ViewSet to register.
    :param related_viewsets: A dictionary of related viewsets for nesting. The value can be a tuple (viewset, related_viewsets, lookup)
    :param lookup: Optional lookup field, defaults to prefix.
    :return: A list of all nested routers' URLs.
    """
    # Register the base viewset
    router.register(prefix, viewset, basename=prefix)

    urlpatterns = Router([])  # Initialize the URL patterns with the base router's URLs

    if related_viewsets:
        lookup = lookup or prefix
        # Create a nested router for this level
        parent_router = routers.NestedSimpleRouter(router, prefix, lookup=lookup)

        for related_prefix, related_viewset_data in related_viewsets.items():
            # Check if related_viewset_data includes a lookup field (tuple with lookup)
            if isinstance(related_viewset_data, tuple):
                if len(related_viewset_data) == 3:
                    related_viewset, sub_related_viewsets, related_lookup = related_viewset_data
                else:
                    related_viewset, sub_related_viewsets = related_viewset_data
                    related_lookup = related_prefix
            else:
                related_viewset = related_viewset_data
                sub_related_viewsets = None
                related_lookup = related_prefix

            # Register the related viewset with the custom lookup
            parent_router.register(related_prefix, related_viewset, basename=f'{prefix}-{related_prefix}')

            # Add the URLs for this parent router to urlpatterns
            urlpatterns.add(parent_router.urls)

            # Recursively register the sub-related viewsets if they exist and append their URLs
            if sub_related_viewsets:
                urlpatterns.add(register_model_routes(parent_router, related_prefix, related_viewset,
                                                     sub_related_viewsets, lookup=related_lookup).urls)


    return urlpatterns

def get_viewset_for_model(model, MODEL_VIEWSET_MAPPING):
    # Get the model name
    model_name = model.__name__
    return MODEL_VIEWSET_MAPPING.get(model_name)


def register_model_routes_auto(router, model, viewset, prefix=None, parent_prefix=None, max_depth=2, current_depth=0, registered_basenames=None, model_stack=None, MODEL_VIEWSET_MAPPING={}):

    if registered_basenames is None:
        registered_basenames = set()

    if model_stack is None:
        model_stack = set()

    if current_depth > max_depth:
        return

    prefix = prefix or slugify(model._meta.model_name)
    basename = f'{parent_prefix}-{prefix}' if parent_prefix else prefix
    lookup = slugify(model._meta.model_name)

    if basename not in registered_basenames:
        router.register(prefix, viewset, basename=basename)
        registered_basenames.add(basename)

    else:
        # If the basename is already registered, skip registration
        return

    # Add the current model to the model_stack to avoid cycles
    model_stack.add(model)

    # Create a nested router for the current model
    parent_router = routers.NestedSimpleRouter(router, prefix, lookup=lookup)

    # Iterate over the fields of the model to find relationships
    for field in model._meta.get_fields():
        if field.is_relation and field.related_model:
            related_model = field.related_model
            if related_model in model_stack:
                continue

            related_viewset = get_viewset_for_model(related_model, MODEL_VIEWSET_MAPPING)

            if related_viewset:
                # Generate a prefix for the related model
                related_prefix = field.name
                related_lookup = related_prefix.replace('-', '_')
                related_basename = f'{basename}-{related_prefix}'
                if related_basename in registered_basenames:
                    continue

                if isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
                    # For ForeignKey and OneToOneField, create a nested route to access the related object
                    parent_router.register(related_prefix, related_viewset, basename=related_basename)
                    registered_basenames.add(related_basename)

                elif isinstance(field, ManyToManyField):
                    # For ManyToManyField, create a nested route to access the related objects
                    parent_router.register(related_prefix, related_viewset, basename=related_basename)
                    registered_basenames.add(related_basename)

                # Recursive call for nested relationships
                register_model_routes_auto(
                    parent_router,
                    related_model,
                    related_viewset,
                    prefix=related_prefix,
                    parent_prefix=basename,
                    max_depth=max_depth,
                    current_depth=current_depth + 1,
                    registered_basenames=registered_basenames,
                    model_stack=model_stack.copy()
                )
            else:
                return parent_router
    # Remove the current model from the model_stack when backtracking
    model_stack.remove(model)


