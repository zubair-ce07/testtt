from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user_management.models import (
    AcademicInformation,
    UserProfile,
    SocialGroup,
    WorkInformation,
    Friend,
    Notification,
    UserGroup,
    GroupRequest,
    FriendRequest
)


class UserProfileSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2', 'date_of_birth', 'phone',
                  'address']

    def save(self, **kwargs):
        userprofile = UserProfile(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            address=self.validated_data['address'],
            phone=self.validated_data['phone'],
            date_of_birth=self.validated_data['date_of_birth'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise ValidationError({'password': 'passwords must match'})

        userprofile.set_password(password)
        userprofile.save()
        return userprofile


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    def get_work_information_url(self, obj):
        return reverse(viewname='work-information') + "?username={}".format(obj.username)

    def get_academic_information_url(self, obj):
        return reverse(viewname='academic-information') + "?username={}".format(obj.username)

    work_information_url = serializers.SerializerMethodField(read_only=True)
    academic_information_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'phone',
                  'address', 'academic_information_url', 'work_information_url']


class WorkInformationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInformation
        exclude = ['user_profile', ]


class WorkInformationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInformation
        fields = '__all__'


class AcademicInformationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInformation
        exclude = ['user_profile', ]


class AcademicInformationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInformation
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialGroup
        fields = '__all__'


class GroupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRequest
        fields = '__all__'


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'


class UserGroupSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user.username')
    name = serializers.StringRelatedField(source='group.name', read_only=True, )

    class Meta:
        model = UserGroup
        fields = ['username', 'name', 'is_admin']


class UserSocialGroupsSerializer(serializers.ModelSerializer):
    social_groups = UserGroupSerializer(source='usergroup_set', read_only=True, many=True)

    class Meta:
        model = UserProfile
        fields = ['social_groups', ]


class UserFriendsSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    user_friends = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'user_friends']

    def get_user_friends(self, obj):
        friends = [UserProfileSerializer(user).data for user in obj.user_friends.all()]
        return friends


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['text', 'status', 'type']
