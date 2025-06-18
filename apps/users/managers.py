from django.contrib.auth.base_user import BaseUserManager
from utils.exceptions import raise_error, ErrorCodes

from apps.users import models as users_models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        users_models.CustomUserPasswordLog.objects.create(user=user, raw_password=password)

        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

    def get_user(self, pk):
        try:
            user = self.get(pk=pk)
            return user
        except self.model.DoesNotExist:
            raise_error(
                ErrorCodes.USER_NOT_FOUND,
                "User not found."
            )

