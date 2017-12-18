from django.contrib.auth.models import User
from rest_framework import serializers

from users.serializers.auth_serializers import LoginSerializer as GenericLoginSerializer, \
    SignupSerializer as GenericSignupSerializer
from users.serializers.user_serializers import UserSerializer as GenericUserSerializer


class UserSerializer(GenericUserSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'userprofile')
        read_only_fields = ('username',)


class LoginSerializer(GenericLoginSerializer):
    password = serializers.CharField(style={'input_type': 'password'})


class SignupSerializer(GenericSignupSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
