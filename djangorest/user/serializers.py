import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('address', 'gender', 'date_of_birth', 'phone_num')


class UserSerializer(serializers.ModelSerializer):
    
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'write_only': True},
                        'last_name': {'write_only': True},
                        'email': {'write_only': True}
                        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user_profile = UserProfile.objects.create(owner=user, **profile_data)
        user_profile.save()
        return user_profile
