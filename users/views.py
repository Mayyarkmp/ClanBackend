from django.db.models import Q
from rest_framework import views
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer
from core.base.viewsets import SuperModelViewSet


class UserViewSet(SuperModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parent_lookup_kwargs = {
        "room_pk": ["rooms__pk"],
        "message_pk": ["sent_messages__sender__pk"],
    }


class SessionView(views.APIView):
    def get(self, request):
        session = request.session
        session["visited"] = True
        return Response({"session_key": session.session_key})
