from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from rest_framework.permissions import BasePermission
from rest_framework import authentication
from rest_framework import status
from users.models import User
from users.models import AppUserToken
from rest_framework.response import Response

def is_authenticated(view_func):
    @wraps(view_func)
    @csrf_exempt
    def wrapped_view(request, *args, **kwargs):
        token = request.headers.get("Authorization",None)
        try:
            app_user_token = AppUserToken.objects.get(key=token)
            request.user = app_user_token.user
            request.user_id = app_user_token.user.user_id
        except (AppUserToken.DoesNotExist, IndexError):
            return JsonResponse({'error': 'Authentication token not valid.'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view

class IsAuthenticatedModular(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        try:
            return bool(request.user and request.user.user_id)
        except Exception as e:
            return False
        
class CustomUserAuth(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        token = request.headers.get("Authorization",None)
        try:
            if token is not None:
                app_user_token = AppUserToken.objects.get(key=token)
                request.user = app_user_token.user
                request.user_id = app_user_token.user.user_id
            else: 
                return None
        except (AppUserToken.DoesNotExist, IndexError):
            return None
        
        if not User.objects.filter(user_id = request.user_id, is_active = True).exists():
            return None
        if request.user is None:
            return None
        return (request.user, None)