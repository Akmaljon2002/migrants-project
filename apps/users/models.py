from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from apps.users.choices import UserRoleChoice
from apps.users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=9,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{9}$',
                message="Phone number must be exactly 9 digits.",
            )
        ],
        help_text="Enter a 9-digit phone number (e.g., 998123456)."
    )
    full_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=UserRoleChoice.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name', 'role']

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name_plural = 'Users'


class CustomUserPasswordLog(models.Model):
    user = models.OneToOneField(CustomUser, related_name="raw_password", on_delete=models.CASCADE)
    raw_password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} - {self.raw_password}"
