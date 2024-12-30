from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from django.http import JsonResponse

class LoginKeyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Allow only for 'login' and 'registration' endpoints
        if not request.path.startswith('/login/') and not request.path.startswith('/register/'):
            if not request.headers.get('Login-Key'):
                return JsonResponse({'detail': 'Login key is required'}, status=401)

    def process_response(self, request, response):
        return response
