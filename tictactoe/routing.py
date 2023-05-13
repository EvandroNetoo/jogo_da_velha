from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/partida/<str:code>', consumers.GameConsumer.as_asgi()),
]