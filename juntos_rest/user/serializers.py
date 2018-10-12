from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Profile


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_superuser', 'date_joined')
        read_only_field = ('is_superuser',)


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'age', 'gender', 'address',)

    def validate_age(self, age):
        if age and age < 0:
            raise ValidationError(_('Age must be positive'))
        return age

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user_serializer.update(instance.user, user_data)

        return super().update(instance, validated_data)
