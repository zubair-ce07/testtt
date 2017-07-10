from django.contrib.auth.models import User

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
    todoitem = TodoItemSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'todoitem')
