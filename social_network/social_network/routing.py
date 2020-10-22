from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# ProtocolTypeRouter will first inspect the type of connection.
# If it is a WebSocket connection (ws:// or wss://),
# the connection will be given to the AuthMiddlewareStack.
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    )

})