import re
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin, ModelViewSet
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver
from django.views import View

from core.settings.models.seo import SEOSettings
from core.settings.serializers import SEOSettingsSerializer


@api_view(["GET"])
def get_supported_languages(request):
    print(request.language)
    supported_languages = [
        {"language": "ar", "name": {"ar": "العربية", "en": "English"}},
        {
            "language": "en",
            "name": {
                "ar": "الانجليزية",
                "en": "English",
            },
        },
    ]

    return Response(supported_languages, status=status.HTTP_200_OK)


def custom_404(request, exception=None):
    response_data = {
        "error": "Not Found",
        "status_code": 404,
        "message": "The resource you are looking for could not be found.",
    }
    return Response(response_data, status=404)


def convert_regex_to_django_pattern(pattern):

    return pattern


def get_view_methods(callback):
    methods = set()

    if hasattr(callback, "cls") and isinstance(callback.cls, APIView):
        methods.update(callback.cls().allowed_methods)

    elif isinstance(callback, ViewSetMixin):
        if hasattr(callback, "actions"):
            for action in callback.actions.keys():
                if action == "list":
                    methods.add("GET")
                elif action == "create":
                    methods.add("POST")
                elif action == "retrieve":
                    methods.add("GET")
                elif action == "update":
                    methods.add("PUT")
                elif action == "partial_update":
                    methods.add("PATCH")
                elif action == "destroy":
                    methods.add("DELETE")
        else:
            methods.update(["GET", "POST", "PUT", "PATCH", "DELETE"])

    elif hasattr(callback, "view_class") and issubclass(callback.view_class, View):
        view_class = callback.view_class
        if hasattr(view_class, "get"):
            methods.add("GET")
        if hasattr(view_class, "post"):
            methods.add("POST")
        if hasattr(view_class, "put"):
            methods.add("PUT")
        if hasattr(view_class, "delete"):
            methods.add("DELETE")
        if hasattr(view_class, "patch"):
            methods.add("PATCH")

    elif hasattr(callback, "__call__"):
        view_func = callback.__name__.lower()
        if "get" in view_func:
            methods.add("GET")
        if "post" in view_func:
            methods.add("POST")
        if "put" in view_func:
            methods.add("PUT")
        if "delete" in view_func:
            methods.add("DELETE")
        if "patch" in view_func:
            methods.add("PATCH")

    if not methods:
        methods.add("GET")

    return list(methods)


@api_view(["GET"])
def get_all_urls(request):
    urls = []

    def list_patterns(patterns, prefix=""):
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                django_pattern = convert_regex_to_django_pattern(str(pattern.pattern))
                callback = pattern.callback
                urls.append(f"/api/v1/{prefix + django_pattern}")

            elif isinstance(pattern, URLResolver):
                # التعامل مع resolvers الفرعية
                list_patterns(pattern.url_patterns, prefix + str(pattern.pattern))

    resolver = get_resolver("clan.api_v1_urls")
    list_patterns(resolver.url_patterns)

    return Response(urls)



@api_view(["GET"])
def get_seo(request):
    seo_content = SEOSettings.objects.filter(is_default=True,is_draft=False).first()
    serializer_data = SEOSettingsSerializer(seo_content).data
    return Response(serializer_data)

