from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.core.validators import RegexValidator
from django_countries.serializer_fields import CountryField

from users.models import UserProfile

message = "Phone number must be entered in the format: '+9999999999'."
phone_validator = RegexValidator(regex=r'^\+?\d{9,15}$', message=message)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='generic:details')
    phone_number = serializers.CharField(source='userprofile.phone_number', validators=[phone_validator], max_length=15,
                                         allow_blank=True, required=False)
    country = CountryField(source='userprofile.country', allow_blank=True, required=False)
    image = serializers.ImageField(allow_empty_file=True, source='userprofile.image', use_url=False)
    address = serializers.CharField(source='userprofile.address', max_length=1000, allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'image', 'address')
        read_only_fields = (
            'id', 'username', 'user_permissions', 'date_joined', 'last_login', 'groups', 'is_superuser', 'is_staff',
            'is_active')
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   password=make_password(validated_data['password']),
                                   email=validated_data['email'],
                                   first_name=validated_data.get('first_name', ''),
                                   last_name=validated_data.get('last_name', ''))
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
