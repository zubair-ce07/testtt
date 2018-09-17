__author__ = 'abdul'
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import serializers as django_serializers
from rest_framework.authtoken.models import Token

from accounts.models import UserProfile, Category
from accounts.helpers import get_user_rating
from feedback.models import Feedback
from report.models import Report


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        try:
            token = Token.objects.get(user__id=user.id)
        except Token.DoesNotExist:
           token = Token.objects.create(user=user)

        role = 'AD' if user.is_staff else user.userprofile.role

        body = {
            'username': user.username,
            'token': token,
            'role' : role,
            'id' : user.id
        }
        return body


class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, min_length=1, label="First Name")
    last_name = serializers.CharField(max_length=30, min_length=1, label="Last Name")
    email_address = serializers.EmailField(min_length=7, label="Email address")
    password = serializers.CharField(style={'input_type': 'password'}, min_length=6, max_length=16, label="Password")

    class Meta:
        model = UserProfile
        # exclude = ['pair']
        fields = ['first_name', 'last_name', 'email_address', 'password', 'cnic_no', 'address', 'city', 'country',
                  'postal_code', 'phone_no', 'role', 'categories', 'display_picture']

    def create(self, validated_data):
        return self.save_user(validated_data)

    def save_user(self, validated_data):
        """ The  user object is created and saved
        """
        new_user = User.objects.create_user(username=validated_data['email_address'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'],
                                            password=validated_data['password'],
                                            email=validated_data['email_address'])
        new_user.save()
        self.save_user_profile(new_user, validated_data)
        return new_user

    def save_user_profile(self, user, validated_data):
        """ The userprofile object that has one-one link with user us created and saved
        """
        user.userprofile.cnic_no = validated_data['cnic_no']
        user.userprofile.phone_no = validated_data['phone_no']
        user.userprofile.address = validated_data['address']
        user.userprofile.city = validated_data['city'].lower()
        user.userprofile.country = validated_data['country'].lower()
        user.userprofile.role = validated_data['role']
        user.userprofile.categories.set(validated_data['categories'])
        user.userprofile.postal_code = validated_data['postal_code']
        user.userprofile.display_picture = validated_data['display_picture']
        user.userprofile.save()


class ProfileViewSerializer(serializers.Serializer):

    def to_representation(self, user):
        return {
            'name' : user.userprofile.full_name(),
            'rating' : get_user_rating(user.userprofile),
            'feedback' : django_serializers.serialize('json', Feedback.objects.filter(given_to_user=user.userprofile))
        }


class UserProfileModelSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        exclude = ()

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name
