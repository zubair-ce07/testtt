from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=1)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        "",
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
