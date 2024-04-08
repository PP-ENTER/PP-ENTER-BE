from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/facechats/(?P<room_id>\d+)/$', consumers.VideoChatConsumer.as_asgi()), # 방번호로 접속합니다.
]
