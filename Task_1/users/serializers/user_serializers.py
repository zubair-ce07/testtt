from django.contrib.auth.models import User
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    country = CountryField(allow_blank=True, required=False)
    image = serializers.ImageField(allow_empty_file=True, use_url=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'country', 'image', 'address')

    def update(self, instance, validated_data):
        if not validated_data.get('image'):
            validated_data.pop('image')
        return super(UserProfileSerializer, self).update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'userprofile')
        read_only_fields = ('username',)

    def update(self, instance, validated_data):
        user_profile_data = validated_data.pop('userprofile')
        profile_serializer = UserProfileSerializer(instance.userprofile, data=user_profile_data)
        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()
        return super(UserSerializer, self).update(instance, validated_data)
