# middleware.py
from urllib.parse import parse_qs
from gameroom.handlers.game_session import get_token_payload

class TokenAuthMiddleware:
    """
    Custom middleware to extract token from headers and set it in the scope.
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token = headers.get(b'authorization', b'').decode('utf-8')
        scope['token_data'] = get_token_payload(token)
        return self.inner(scope, receive, send)

# Middleware stack for ASGI
def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)

# Middleware for WSGI (Django REST API)
class TokenAuthMiddlewareWSGI:
    """
    Middleware to extract token from headers for HTTP requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization', '')
        request.token_data = get_token_payload(token).get('data', {})
        response = self.get_response(request)
        return response