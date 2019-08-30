"""core serializer module."""
from rest_framework import serializers
from django.contrib.auth.models import User

from shop.models import Saloon
from customer.models import Customer


class UserSerializer(serializers.ModelSerializer):
    """core app user serializer for user registration"""

    password1 = serializers.CharField(write_only=True, source='password')
    password2 = serializers.CharField(write_only=True)
    user_type = serializers.CharField(write_only=True)

    class Meta:
        """UserSerializer meta class."""

        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2', 'user_type')

    def create(self, validated_data):
        """UserSerializer create method override"""
        validated_data.pop('password2')
        user_type = validated_data.pop('user_type')
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if user_type == 'customer':
            Customer.objects.create(user=user)
        else:
            Saloon.objects.create(user=user)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """core app user serializer for user update"""
    class Meta:
        """UserUpdateSerializer meta class"""
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username')
