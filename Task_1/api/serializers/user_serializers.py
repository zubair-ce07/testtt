from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from users.models import UserProfile


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    country = CountryField(allow_blank=True, required=False)

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'country', 'image', 'address',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(style={'placeholder': 'Username'})
    password = serializers.CharField(style={'placeholder': 'Password', 'input_type': 'password'})
