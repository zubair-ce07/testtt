from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import UserProfile

message = "Phone number must be entered in the format: '+9999999999'."
phone_validator = RegexValidator(regex=r'^\+?\d{9,15}$', message=message)


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='generic:details')
    phone_number = serializers.CharField(source='userprofile.phone_number', max_length=15,
                                         allow_blank=True, required=False)
    country = CountryField(source='userprofile.country', allow_blank=True, required=False)
    image = serializers.ImageField(allow_empty_file=True, source='userprofile.image', use_url=False, allow_null=True)
    address = serializers.CharField(source='userprofile.address', max_length=1000, allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'image', 'address')


class SignupSerializer(UserSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'image',
            'address')

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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
