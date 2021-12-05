from django.urls import re_path

from django.conf.urls import include

from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>[\w-]{,50})/$', consumers.ChatConsumer.as_asgi()),
]
# ASGI 애플리케이션을 얻기 위해 클래스 메서드인 as_asgi()를 호출하여 이 애플리케이션이 각 유저별 연결을 처리하는 컨슈머 인스턴스를 만들어준다.
