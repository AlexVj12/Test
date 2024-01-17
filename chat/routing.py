from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import ChatConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"ws/chat/", ChatConsumer.as_asgi()),
]
