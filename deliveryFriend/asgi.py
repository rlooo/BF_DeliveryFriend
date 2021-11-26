"""
ASGI config for deliveryFriend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

# 최상단 라우팅 설정이 chat.rouing 모듈을 가리키도록 한다.
# 연결이 웹소켓 타입이라면 (ws://나 wss://) 이 연결은 AuthMiddlewareStack으로 전달된다.
# AuthMiddlewareStack은 현재 인증된 유저에 대한 참조를 연결의 scope에 추가한다.
# 후에 이 연결은 URLRouter에게 전달된다. URLRouter는 연결의 HTTP 경로를 확인해 적절한 컨슈머에게 연결해준다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deliveryFriend.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
