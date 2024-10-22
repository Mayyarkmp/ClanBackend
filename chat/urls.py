from rest_framework_nested import routers

from users.views import UserViewSet
from .views import RoomViewSet, MessageViewSet
from core.base.routers import register_model_routes
app_name = 'chat'
router = routers.DefaultRouter()
room_router = register_model_routes(router, "rooms", RoomViewSet, {
    "messages": MessageViewSet,
    "members": UserViewSet,
}, "room")

message_router = register_model_routes(router, "messages", MessageViewSet, {
    "sender": UserViewSet,
    # "receivers": UserViewSet,
}, "message")
urlpatterns = router.urls
urlpatterns += room_router.urls
urlpatterns += message_router.urls