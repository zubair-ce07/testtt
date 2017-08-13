from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

message = "Phone number must be entered in the format: '+9999999999'."
phone_validator = RegexValidator(regex=r'^\+?\d{9,15}$', message=message)


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='generic:details')
    phone_number = serializers.CharField(source='userprofile.phone_number', max_length=15, validators=[phone_validator],
                                         allow_blank=True, required=False)
    country = CountryField(source='userprofile.country', allow_blank=True, required=False)
    image = serializers.ImageField(allow_empty_file=True, source='userprofile.image', use_url=False, allow_null=True)
    address = serializers.CharField(source='userprofile.address', max_length=1000, allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'image', 'address')
        read_only_fields = ('username',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
