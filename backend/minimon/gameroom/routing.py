from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/gameroom/<str:room_name>', consumers.GameRoomConsumer.as_asgi()),
]
