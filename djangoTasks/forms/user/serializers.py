import datetime
import re

from rest_framework import serializers
from django.contrib.auth import get_user_model

from forms.messages import ErrorMessages
from user import models

USER = get_user_model()

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        exclude = ['groups', 'user_permissions']
        write_only_fields = ('password', )
        read_only_fields = (
            'id', 'last_login', 'date_joined', 'is_active', 'is_staff'
        )

    def validate_first_name(self, value):
        if re.match('^[a-zA-Z ]+$', value):
            return value
        raise serializers.ValidationError(ErrorMessages.INVALID_NAME_ERROR)

    def validate_last_name(self, value):
        if re.match('^[a-zA-Z ]+$', value):
            return value
        raise serializers.ValidationError(ErrorMessages.INVALID_NAME_ERROR)

    def validate_email(self, value):
        if USER.objects.filter(email=value).exists():
            raise serializers.ValidationError(ErrorMessages.EMAIL_EXISTS)
        return value


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Product
        fields = '__all__'

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return price


class UserProfileSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()

    class Meta:
        model = models.UserProfile
        depth = 1
        fields = '__all__'
        read_only_fields = ('age', )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = USER.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        profile = models.UserProfile.objects.create(
            user=user,
            **validated_data
        )
        return profile

    def validate(self, data):
        # validate true if age is greater than 18
        today = datetime.date.today()
        birthday = data['birthday']
        age = today.year - birthday.year
        if today.month < birthday.month or today.month == birthday.month\
                and today.day < birthday.day:
            age = age - 1
        if age < 18:
            raise serializers.ValidationError("Age must be greater 18")
        return data
