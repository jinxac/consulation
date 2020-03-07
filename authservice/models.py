from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import UserManager


class RoleType(models.IntegerChoices):
    Doctor = 0
    Assistant = 1
    Client = 2
    Admin = 3


class User(AbstractBaseUser, PermissionsMixin):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    dob = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    role = models.IntegerField(RoleType.choices, default=RoleType.Assistant)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return None

    def get_short_name(self):
        return None

