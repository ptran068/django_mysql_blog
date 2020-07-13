from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRoute
from posts import routing as posts_routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            posts_routing.websocket_urlpatterns
        )
    ),
})