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
        fields = ['id', 'memory_title', 'datetime', 'activity', 'user']


class UserSerializer(serializers.ModelSerializer):
    mems = MemorySerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'username', 'image',
                  'password', 'categories', 'activities', 'mems']

