from django.contrib.auth.models import User
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django_countries.fields import CountryField

from users.models import UserProfile


class UserSerializer(serializers.ModelSerializer, CountryFieldMixin):
    address = serializers.CharField(source='userprofile.address', allow_blank=True)
    phone_number = serializers.CharField(source='userprofile.phone_number', allow_blank=True)
    image = serializers.ImageField(source='userprofile.image', allow_empty_file=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'image',)

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile', None)
        user = super(UserSerializer, self).create(validated_data)
        self.update_or_create_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', None)
        self.update_or_create_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def update_or_create_profile(self, user, profile_data):
        # This always creates a Profile if the User is missing one;
        # change the logic here if that's not right for your app
        UserProfile.objects.update_or_create(user=user, defaults=profile_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'country', 'address', 'image', 'user']
