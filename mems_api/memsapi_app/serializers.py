from memsapi_app.models import User, Memory, Activity, Category
from rest_framework import serializers



class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'title', 'text', 'url', 'tags', 'is_public', 'image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'memory_title', 'datetime', 'activity']


class UserSerializer(serializers.ModelSerializer):
    mems = MemorySerializer(many=True)
    categories = CategorySerializer(many=True)
    activities = ActivitySerializer(many=True)
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'username',
                  'password', 'categories', 'activities', 'mems']

