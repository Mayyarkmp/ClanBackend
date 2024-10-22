from django.urls import path
from .views import FileUploadView, MediaViewSet, LinkImageView, CheckObjectExistenceView
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register(r"", MediaViewSet)


app_name = "media"

urlpatterns = [
    path("upload/", FileUploadView.as_view(), name="upload"),
    path("link/", LinkImageView.as_view(), name="link"),
    path(
        "check-object/",
        CheckObjectExistenceView.as_view(),
        name="check-object-existence",
    ),
]

urlpatterns += router.urls
