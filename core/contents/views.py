from .serializers import DeliveryTypeContentsSerializer
from .models import DeliveryTypeContents
from core.base.viewsets import SuperModelViewSet


class DeliveryTypeContentsViewSet(SuperModelViewSet):
    queryset = DeliveryTypeContents.objects.all()
    serializer_class = DeliveryTypeContentsSerializer
