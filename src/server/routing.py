from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from product import routing
from channels.security.websocket import AllowedHostsOriginValidator


# =============================== ASGI Routing ===================================

application = ProtocolTypeRouter({
    'websocket':
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )


})

# ============================= END ASGI Routing =================================
