from django.db import models
from rest_framework.response import Response
from apps.users.filters import UserFilter
from utils.exceptions import raise_error, ErrorCodes
from utils.pagination import BaseService, BaseServicePagination
from apps.users import serializers as slr
from apps.users import models as users_models


class UserAuthService(BaseService):

    def login(self):
        serializer = slr.LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user, refresh = serializer.validated_data
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': slr.CustomUserSerializer(user).data
        })

    def logout(self):
        serializer = slr.LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=204)


class UserService(BaseServicePagination):

    def create_user(self):
        serializer = slr.CustomUserCreateSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(slr.CustomUserSerializer(user).data, status=201)

    def update_user(self, pk):
        serializer = slr.CustomUserUpdateSerializer(
            self._get_user(pk),
            data=self.request.data,
            context = {'request': self.request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

    def list_users(self):
        request = self.request
        users = users_models.CustomUser.objects

        filterset = UserFilter(self.request.GET, queryset=users.all().order_by('-created_at'))
        if filterset.is_valid():
            users = filterset.qs
        results = self.paginate(users)
        serializer = slr.CustomUserSerializer(
            results,
            many=True
        )
        return self.paginated_response(serializer.data)

    def get_user(self, pk):
        serializer = slr.CustomUserSerializer(
            self._get_user(pk)
        )
        return Response(serializer.data)

    def get_current_user(self):
        serializer = slr.CustomUserSerializer(
            self.request.users
        )
        return Response(serializer.data)

    def delete_user(self, pk):
        user = self._get_user(pk)
        user.delete()
        return Response(status=204)

    def _get_user(self, pk):
        try:
            user = users_models.CustomUser.objects
            user = user.get(id=pk)
        except users_models.CustomUser.DoesNotExist:
            raise_error(
                ErrorCodes.USER_NOT_FOUND,
                "User not found."
            )
        return user


