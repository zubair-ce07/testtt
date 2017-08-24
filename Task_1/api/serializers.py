from django.contrib.auth.models import User
from rest_framework import serializers

from users.serializers.auth_serializers import LoginSerializer as lSerializer, SignupSerializer as sSerializer
from users.serializers.user_serializers import UserSerializer as uSerializer


class UserSerializer(uSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'userprofile')
        read_only_fields = ('username',)


class LoginSerializer(lSerializer):
    password = serializers.CharField(style={'input_type': 'password'})


class SignupSerializer(sSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
