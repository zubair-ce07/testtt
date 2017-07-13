from rest_framework import serializers
from .models import CustomUser, Task


class CustomUsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.ReadOnlyField(source='self.is_superuser')

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'profile_picture', 'city', 'email', 'is_superuser']
        lookup_field = 'username'

    def create(self, validated_data):
        user = super(CustomUsersSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UsersTaskSerializer(serializers.ModelSerializer):
    user = CustomUsersSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'dated', 'user']

