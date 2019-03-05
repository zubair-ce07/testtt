from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token
from rest_framework import exceptions


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)

    @staticmethod
    def authenticate(username, password):
        user = authenticate(username=username, password=password)

        if not user:
            raise exceptions.AuthenticationFailed(
                {'error': 'username or password is incorrect'})

        token, _ = Token.objects.get_or_create(user=user)

        return (user, token)
