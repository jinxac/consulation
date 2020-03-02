
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email):
        if not email:
            raise ValueError('Email must be set!')
        user = self.model(email=email)
        user.save(using=self._db)
        return user
