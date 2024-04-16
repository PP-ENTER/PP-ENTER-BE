from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/facechats/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()), # 방번호로 접속합니다.
    re_path(r'ws/call/', consumers.CallConsumer.as_asgi()),
    # re_path(r'ws/invite/', consumers.ChatConsumer.as_asgi()),
	re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi())
]


# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })