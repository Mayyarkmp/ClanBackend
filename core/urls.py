from django.urls import path, include
from . import views


app_name = "core"

urlpatterns = [
    path("languages/", views.get_supported_languages, name="supported_languages"),
    path("media/", include("core.media.urls", namespace="media")),
    path("settings/", include("core.settings.urls", namespace="settings")),
    path("urls/", views.get_all_urls),
    path('contents/', include('core.contents.urls', namespace='contents')),
    path('seo/', views.get_seo, name='seo')
]
