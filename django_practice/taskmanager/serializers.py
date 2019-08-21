from rest_framework import serializers

from taskmanager.models import Task, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'birthday', 'address',)


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer()
    assigned_by = UserSerializer()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'status', 'assignee', 'assigned_by', )
