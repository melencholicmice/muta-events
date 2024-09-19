import jwt
import re
from user.models import User
from rest_framework.response import Response
from muta_event.settings import COOKIE_ENCRYPTION_SECRET

class UserAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = [
            '/event/create-event',
            '/event/get-all-events-by-user',
            '^/get-all-attendees-by-event/[0-9a-fA-F-]{36}/$',
        ]

    def __call__(self, request):
        response = Response()
        user = None
        path_match = False

        for patterns in self.protected_paths:
            if request.path == patterns or re.match(patterns, request.path):
                path_match = True
                break

        if path_match:
            token = request.headers.get('Authorization')
            if not token:
                response.data = {"message":"User not authenticated"}
                response.status_code = 403
                return response

            try:
                payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
                user = User.objects.get(user_id=payload["user_id"])
                if not user:
                    response.data = {"message":"User not authenticated"}
                    response.status_code = 403
                    return response
            except Exception as e:
                response.data = {"message":"User not authenticated"}
                response.status_code = 403
                return response
            
        if not user.is_email_verified:
            response.data = {"message":"Please verify your email"}
            response.status_code = 403
            return response
            
        request.user = user
        response = self.get_response(request)
        return response
