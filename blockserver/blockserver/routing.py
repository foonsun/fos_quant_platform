from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import wslog.routing

application = ProtocolTypeRouter({
    # empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
            URLRouter(
                    wslog.routing.websocket_urlpatterns
                )
        ),
    })