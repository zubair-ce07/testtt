from rest_framework import serializers
from .models import CustomUser, Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser Model
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'profile_picture', 'city', 'email', 'is_superuser']
        read_only_fields = ('is_superuser',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UsersTaskSerializer(serializers.ModelSerializer):
    """
        Serializer for Task Model
        """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'due_date', 'user']

