from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.user_serializers import UserSerializer
from users.models import UserProfile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(style={'placeholder': 'Username'})
    password = serializers.CharField(style={'placeholder': 'Password', 'input_type': 'password'})


class SignupSerializer(UserSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, )
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'userprofile')

    def create(self, validated_data):
        user_profile_data = validated_data.pop('userprofile')
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super(SignupSerializer, self).create(validated_data)
        user_profile = UserProfile(user=user, phone_number=user_profile_data.get('phone_number'),
                                   country=user_profile_data.get('country'),
                                   address=user_profile_data.get('address'),
                                   image=user_profile_data.get('image'))
        user_profile.full_clean()
        user_profile.save()
        return user

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError({'password': 'The passwords do not match'})
        validate_password(password=password1)
        return super(SignupSerializer, self).validate(attrs)
