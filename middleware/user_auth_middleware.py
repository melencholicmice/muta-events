import jwt
import re
from django.http import JsonResponse
from user.models import User

from muta_event.settings import COOKIE_ENCRYPTION_SECRET

class UserAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = [
            '/event/create-event',
            '/event/get-all-events-by-user',
            '^/event/get-all-attendees-by-event/[0-9a-fA-F-]{36}$',
        ]

    def __call__(self, request):
        user = None
        path_match = False

        for patterns in self.protected_paths:
            if request.path == patterns or re.match(patterns, request.path):
                path_match = True
                break

        if path_match:
            token = request.headers.get('Authorization')

            if token and token.startswith('Bearer '):
                token = token.split(' ')[1]

            if not token:
                return JsonResponse({"message": "User not authenticated"}, status=403)

            try:
                payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
                user = User.objects.get(user_id=payload["user_id"])
                if not user:
                    return JsonResponse({"message": "User not authenticated"}, status=403)
            except Exception as e:
                return JsonResponse({"message": "User not authenticated"}, status=403)
            
            if not user.is_email_verified:
                return JsonResponse({"message": "Please verify your email"}, status=403)
            
        request.muta_user = user
        response = self.get_response(request)
        return response