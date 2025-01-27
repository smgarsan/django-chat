from django.urls import path
from .consumers import UserConsumer

websocket_urlpatterns = [
    path("ws/user/", UserConsumer.as_asgi()),
]