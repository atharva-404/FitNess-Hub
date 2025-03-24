from django.urls import re_path
from trainer.consumer import VideoConsumer

websocket_urlpatterns = [
    re_path(r'ws/trainer/$', VideoConsumer.as_asgi()),
]

