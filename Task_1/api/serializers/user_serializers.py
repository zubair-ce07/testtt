from django.contrib.auth.models import User
from django_countries.fields import Country
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    country = CountryField(allow_blank=True, required=False)
    image = serializers.ImageField(allow_empty_file=True, use_url=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'country', 'image', 'address')


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'userprofile')
        read_only_fields = ('username',)

    def update(self, instance, validated_data):
        user_profile = instance.userprofile
        user_profile_data = validated_data.pop('userprofile')
        user_profile.phone_number = user_profile_data.get('phone_number')
        user_profile.country = Country(code=user_profile_data.get('country'))
        user_profile.address = user_profile_data.get('address')
        if user_profile_data.get('image'):
            user_profile.image = user_profile_data.get('image')
        user_profile.save()
        return super(UserSerializer, self).update(instance, validated_data)
