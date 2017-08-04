from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

from users.models import UserProfile
from api.serializers.edit_serializer import EditSerializer


class SignupSerializer(EditSerializer):
    username = serializers.CharField(source='user.username', style={
        'placeholder': '150 characters or fewer. Letters, digits and @/./+/-/_ only.'}, validators=[
        UniqueValidator(queryset=User.objects.all(), message='A user with that username already exists'),
        UnicodeUsernameValidator()])
    password1 = serializers.CharField(source='user.password', write_only=True,
                                      style={'input_type': 'password', 'placeholder': 'Enter Password'}, )
    password2 = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Confirm Password'},
                                      write_only=True)

    def create(self, validated_data):
        user_data = validated_data.get('user')
        user = User(username=user_data.get('username'),
                    password=make_password(user_data.get('password')),
                    email=user_data.get('email'),
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name'))
        user.full_clean()
        user.save()
        validated_data['user'] = user
        user_profile = super(SignupSerializer, self).create(validated_data)
        user_profile.full_clean()
        return user_profile

    def validate(self, attrs):
        password1 = attrs.get('user').get('password')
        password2 = attrs.pop('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError({'password1': 'The passwords do not match'})
        if validate_password(password=password1):
            raise ValidationError({'password1': 'Weak Password'})
        return super(SignupSerializer, self).validate(attrs)

    class Meta:
        model = UserProfile
        fields = (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phone_number', 'address',
            'image', 'country',)
