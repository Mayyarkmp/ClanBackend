from rest_framework_nested import routers

from chat.views import MessageViewSet
from core.base.routers import register_model_routes
from customers.chat.views import RoomViewSet

app_name = 'chat'

router = routers.DefaultRouter()

room_router = register_model_routes(router, "rooms", RoomViewSet, {
    'messages': MessageViewSet
}, "room")
urlpatterns = []
urlpatterns += router.urls
urlpatterns += room_router.urls