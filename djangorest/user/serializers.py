from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('phone_num', 'address', 'date_of_birth', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(owner=user, **profile_data)
        return user


