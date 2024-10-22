import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from .middlewares.channels import JWTAuthMiddleware
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from orders.routing import websocket_urlpatterns as order_websocket_urlpatterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clan.settings')

django_asgi_app = get_asgi_application()
websocket_urlpatterns = []
websocket_urlpatterns += chat_websocket_urlpatterns
websocket_urlpatterns += order_websocket_urlpatterns

application = ProtocolTypeRouter(dict(http=django_asgi_app, websocket=JWTAuthMiddleware(
    URLRouter(websocket_urlpatterns)
)))
