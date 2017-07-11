from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
from rest_framework.response import Response

from todo.models import TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    """
    Model Serializer for TodoItem Model
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = TodoItem
        fields = ('description', 'user', 'date_created',
                  'status', 'date_completed', )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user class
    """
    todoitem = TodoItemSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'todoitem')

    def create(self, validated_data, *args, **kwargs):
        """
        Create and return a new `User` instance, given the validated data.
        """
        todo_data = validated_data.get('todoitem')
        user = User.objects.create_user(validated_data['username'])
        for item in todo_data:
            TodoItem.objects.create(user=user, **item)
        return user
