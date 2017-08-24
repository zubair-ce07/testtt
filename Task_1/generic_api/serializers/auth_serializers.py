from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from generic_api.serializers.user_serializers import UserSerializer, UserProfileSerializer


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password',)


class SignupSerializer(UserSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'userprofile')

    def create(self, validated_data):
        user_profile_data = validated_data.pop('userprofile')
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super(SignupSerializer, self).create(validated_data)
        profile_serializer = UserProfileSerializer(data=user_profile_data)
        if profile_serializer.is_valid():
            profile_serializer.validated_data.update({'user': user})
            profile_serializer.save()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password and password2 and password != password2:
            raise ValidationError({'password': 'The passwords do not match'})
        validate_password(password=password)
        return super(SignupSerializer, self).validate(attrs)
