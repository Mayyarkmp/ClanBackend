from rest_framework_nested import routers

from chat.views import RoomViewSet, MessageViewSet
from users.views import SessionView, UserViewSet
from django.urls import path
from core.base.routers import register_model_routes
app_name = 'users'

router = routers.DefaultRouter()

user_router = register_model_routes(router, '', UserViewSet, {
    'rooms': RoomViewSet,
    'messages': MessageViewSet,
}, "user")

urlpatterns = [
    path('session/', SessionView.as_view()),

]
urlpatterns += router.urls
urlpatterns += user_router.urls
