from django.urls import re_path

from django.conf.urls import include

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<label>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# channel_routing = [
#     route("websocket.connect", ws_connect),
#     route("websocket.receive", ws_receive),
#     route("websocket.disconnect", ws_disconnect),
# ]