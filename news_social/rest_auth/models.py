from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django_extensions.db.models import TimeStampedModel
from rest_framework.authtoken.models import Token

from rest_auth.model_manager import CustomUserManager


class CustomUser(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="User Email", unique=True)
    first_name = models.CharField(null=False, blank=False, max_length=50)
    last_name = models.CharField(null=True, blank=True, max_length=50)
    phone = models.CharField(null=True, blank=True, max_length=15)
    password = models.CharField(null=False, blank=False, max_length=500)
    is_active = models.BooleanField(default=True,
                                    help_text="Designates whether this user should be treated as active. "
                                              "Unselect this instead of deleting accounts.")
    date_joined = models.DateTimeField(default=datetime.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"


class User(CustomUser):
    class Meta(CustomUser.Meta):
        swappable = "AUTH_USER_MODEL"


class TokenModel(Token):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_auth_tokens",
        on_delete=models.CASCADE,
        verbose_name="User Token"
    )
