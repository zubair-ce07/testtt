from django.contrib.auth.models import User
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator, ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator

from users.models import UserProfile


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    country = serializers.CharField(source='country.name')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'country', 'image', 'address',)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(style={'placeholder': 'Username'})
    password = serializers.CharField(style={'placeholder': 'Password', 'input_type': 'password'})


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=20, source='user.first_name', required=False, allow_blank=True,
                                       style={'placeholder': 'e.g. John (Optional)'})
    last_name = serializers.CharField(max_length=20, source='user.last_name', required=False, allow_blank=True,
                                      style={'placeholder': 'e.g. Doe (Optional)'})
    email = serializers.EmailField(source='user.email', style={'placeholder': 'Email Address'})

    def update(self, instance, validated_data):
        if not validated_data.get('image'):
            validated_data.pop('image')
        user = self.instance.user
        user_data = validated_data.pop('user')
        user.email = user_data.pop('email')
        user.first_name = user_data.pop('first_name')
        user.last_name = user_data.pop('last_name')
        user.save()
        return super(UserProfileSerializer, self).update(instance, validated_data)

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'address', 'image', 'country',)


class SignupSerializer(UserProfileSerializer):
    username = serializers.CharField(source='user.username', style={
        'placeholder': '150 characters or fewer. Letters, digits and @/./+/-/_ only.'}, validators=[
        UniqueValidator(queryset=User.objects.all(), message='A user with that username already exists'),
        UnicodeUsernameValidator()])
    password1 = serializers.CharField(source='user.password', write_only=True,
                                      style={'input_type': 'password', 'placeholder': 'Enter Password'}, )
    password2 = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Confirm Password'},
                                      write_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user_data = validated_data.get('user')
        user = User(username=user_data.pop('username'),
                    password=make_password(user_data.pop('password')),
                    email=user_data.pop('email'),
                    first_name=user_data.pop('first_name'),
                    last_name=user_data.pop('last_name'))
        user.full_clean()
        user.save()
        validated_data['user'] = user
        userprofile = super(SignupSerializer, self).create(validated_data)
        userprofile.full_clean()
        return userprofile

    def validate(self, attrs):
        password1 = attrs.get('user').get('password')
        password2 = attrs.pop('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError({'password1': 'The passwords do not match'})
        if validate_password(password=password1):
            raise ValidationError('Weak Password')
        return super(SignupSerializer, self).validate(attrs)

    class Meta:
        model = UserProfile
        fields = (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phone_number', 'address',
            'image', 'country',)
