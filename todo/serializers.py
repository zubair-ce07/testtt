from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from todo.models import TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    """
    Model Serializer for TodoItem Model
    """
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
        fields = ('id', 'username', 'todoitem')
