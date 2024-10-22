from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from core.base.viewsets import SuperModelViewSet

class RoomViewSet(SuperModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    parent_lookup_kwargs = {
        "central_user_pk": ["members__pk"],
        "user_pk": ["members__pk"]
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        data["members"].append(request.user.id)
        data["creator"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




class MessageViewSet(SuperModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    parent_lookup_kwargs = {
        "room_pk": ["room__pk"],
        "central_user_pk": ["sender__pk"],
        "user_pk": ["members__pk"]
    }


