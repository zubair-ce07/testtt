from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault
from ContactTodoManagement.models import User, Todo, Contact, Item
from django.shortcuts import get_object_or_404


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'phone_number', 'email', 'country', 'password']
        read_only_fields = ['pk']
        extra_kwargs = {'password': {'write_only': True}}


class ContactSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Contact
        fields = ['pk', 'user', 'name', 'email', 'phone_number', 'country', 'profile_img']
        read_only_fields = ['pk', 'user']


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ['pk', 'todo', 'text', 'status', 'due_date']


class TodoSerializer(ModelSerializer):
    Items = ItemSerializer(many=True)
    user = HiddenField(default=CurrentUserDefault())

    def create(self, validated_data):
        Items = validated_data.pop('Items')
        todo = Todo()
        todo.title = validated_data.get('title')
        todo.status = validated_data.get('status')
        todo.user = validated_data.get('user')
        todo.save()

        for item in Items:
            todo_item = Item()
            todo_item.todo = todo
            todo_item.text = item.get('text')
            todo_item.status = item.get('status')
            todo_item.due_date = item.get('due_date')
            todo_item.save()

        return todo

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        kwargs_data = self._kwargs.get('data')
        items_received = kwargs_data.get('Items')

        if items_received:
            for item_received in items_received:
                item_id_received = item_received.get('pk')
                item = get_object_or_404(Item, id=item_id_received)
                if item:
                    item.status = item_received.get('status', item.status)
                    item.text = item_received.get('text', item.text)
                    item.due_date = item_received.get('due_date', item.due_date)
                    item.save()

        return instance

    class Meta:
        model = Todo
        fields = ['pk', 'user', 'title', 'status', 'Items']
        read_only_fields = ['pk', 'user']
