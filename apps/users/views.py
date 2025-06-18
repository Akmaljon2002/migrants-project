from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.users import services as svc
from apps.users import schemas as scm
from apps.users.check_auth import IPThrottle, permission
from apps.users.schemas import create_user_scm, list_users_scm, get_user_schema, update_user_schema, delete_user_schema, \
    get_current_user_schema


@scm.login_scm
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([IPThrottle])
def login(request):
    return svc.UserAuthService(request).login()


@scm.logout_scm
@api_view(['DELETE'])
@throttle_classes([IPThrottle])
def logout(request):
    return svc.UserAuthService(request).logout()


@create_user_scm
@api_view(['POST'])
@permission(['admin', 'operator'])
def create_user(request):
    return svc.UserService(request).create_user()


@list_users_scm
@api_view(['GET'])
@permission(['admin', 'operator'])
def list_users(request):
    return svc.UserService(request).list_users()


@get_user_schema
@api_view(['GET'])
@permission(['admin', 'operator'])
def get_user(request, pk):
    return svc.UserService(request).get_user(pk)


@get_current_user_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    return svc.UserService(request).get_current_user()


@update_user_schema
@api_view(['PUT'])
@permission(['admin', 'operator'])
def update_user(request, pk):
    return svc.UserService(request).update_user(pk)


@delete_user_schema
@api_view(['DELETE'])
@permission(['admin', 'operator'])
def delete_user(request, pk):
    return svc.UserService(request).delete_user(pk)