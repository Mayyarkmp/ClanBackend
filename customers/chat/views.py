from chat.serializers import RoomSerializer
from core.base.viewsets import SuperReadOnlyModelViewSet
from chat.models import Room

class RoomViewSet(SuperReadOnlyModelViewSet):
    permission_classes = []
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    def get_queryset(self):
        print(self.request.user)
        return self.queryset.filter(members__in=[self.request.user])



