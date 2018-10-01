from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault
from ContactTodoManagement.models import User, Todo, Contact, Item
from django.shortcuts import get_object_or_404


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'phone_number', 'email', 'country', 'password']
        read_only_fields = ['pk']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        password = validated_data.get('password', '')
        user.set_password(password)
        user.save()
        return user


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
        read_only_fields = ['pk']


class TodoItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ['pk', 'text', 'status', 'due_date']
        read_only_fields = ['pk']


class TodoSerializer(ModelSerializer):
    Items = TodoItemSerializer(many=True)
    user = HiddenField(default=CurrentUserDefault())

    def create(self, validated_data):

        items_received = validated_data.pop('Items')
        items = []
        todo = Todo.objects.create(**validated_data)
        for item in items_received:
            item['todo'] = todo
            items.append(Item(**item))
        Item.objects.bulk_create(items)

        return todo

    def update(self, instance, validated_data):

        instance.update_todo(validated_data)

        kwargs = self._kwargs.get('data')
        items = kwargs.get('Items') if kwargs else None

        if items:
            for item_received in items:
                item_id = item_received.get('pk')
                item = get_object_or_404(Item, id=item_id)
                if item:
                    item.update_item(item_received)
                else:
                    raise item
        return instance

    class Meta:
        model = Todo
        fields = ['pk', 'user', 'title', 'status', 'Items']
        read_only_fields = ['pk', 'user']
