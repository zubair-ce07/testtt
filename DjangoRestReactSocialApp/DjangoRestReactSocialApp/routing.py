from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from social_app.consumers import NotificationConsumer
application = ProtocolTypeRouter({
    'websocket':
        AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path("social/<username>", NotificationConsumer),
                    path("socket.io/", NotificationConsumer),
                    url(r"^(social/<username>[\w.@+-]+)/", NotificationConsumer),
                    url(r"^(socket.io/[\w.@+-]+)/", NotificationConsumer),
                ]
            )
        )
    )
})