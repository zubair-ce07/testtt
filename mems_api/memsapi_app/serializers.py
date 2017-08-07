from memsapi_app.models import User, Memory, Activity, Category
from rest_framework import serializers



class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'title', 'text', 'url', 'tags', 'is_public', 'image', 'user', 'category']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'user']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'memory_title', 'datetime', 'activity']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'username', 'image',
                  'password']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required='required'),
    password = serializers.CharField(max_length=200)