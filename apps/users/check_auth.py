from random import randint
from functools import wraps
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class IPThrottle(UserRateThrottle):
    rate = '5/min'


def generate_sms_code():
    return randint(1000, 9999)

def get_access_token(user):
    token = AccessToken.for_user(user)
    token.set_exp(lifetime=timedelta(days=365))
    return str(token)

def get_refresh_token(phone, password):
    user = authenticate(phone=phone, password=password)
    if not user:
        raise AuthenticationFailed('Invalid phone or password.')
    return user, RefreshToken.for_user(user)

def blacklist(refresh):
    token = RefreshToken(refresh)
    token.blacklist()
    return True

def allowed_only_admin():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return Response({'detail': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator

def permission(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                return Response({'detail': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator

