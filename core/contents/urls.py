from rest_framework_nested import routers
from .views import DeliveryTypeContentsViewSet

app_name = 'contents'

router = routers.DefaultRouter()


router.register(r'delivery-types', DeliveryTypeContentsViewSet)



urlpatterns = []
urlpatterns += router.urls