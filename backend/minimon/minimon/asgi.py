"""
ASGI config for minimon project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from minimon.middleware.token import TokenAuthMiddlewareStack
import chatroom.routing
import gameroom.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minimon.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":TokenAuthMiddlewareStack(
                AuthMiddlewareStack(URLRouter(
            chatroom.routing.websocket_urlpatterns +
            gameroom.routing.websocket_urlpatterns
            )
        )
    )     
})
