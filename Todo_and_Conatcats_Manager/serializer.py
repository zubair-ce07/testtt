from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone

from system.models import Contact, Item, Todo


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password', 'phone_number',
            'country', 'profile_picture', 'date_joined'
        ]
        read_only_fields = ['date_joined']

    def validate(self, object):
        object['password'] = make_password(object['password'])
        return object


class ContactListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        context = self._kwargs.get("context")
        request = context.get("request")
        user = request.user
        loop = [Contact(user=user, **n) for n in validated_data]
        return Contact.objects.bulk_create(loop)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = ContactListSerializer
        model = Contact
        exclude = ('user',)
        read_only_fields = ['pk', 'created_at']

    def create(self, validated_data):
        context = self._kwargs.get("context")
        request = context.get("request")
        user = request.user
        return Contact.objects.create(user=user, **validated_data)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id', 'todo']

    def validate(self, object):
        current_datetime = datetime.now(timezone.utc)
        if object.get('due_date') <= current_datetime:
            raise serializers.ValidationError(
                {'due_date': 'should be greater than current date-time'})
        return object

    def create(self, validated_data):
        todo_pk = self.context.get("todo_pk")
        todo_obj = Todo.objects.get(pk=todo_pk)
        return Item.objects.create(todo=todo_obj, **validated_data)


class TodoSerializer(serializers.ModelSerializer):
    todo = ItemSerializer(many=True)

    class Meta:
        model = Todo
        fields = ('pk', 'title', 'todo')
        read_only_fields = ['pk']

    def create(self, validated_data):
        context = self._kwargs.get("context")
        request = context.get("request")
        user = request.user
        item_data = validated_data.pop("todo")
        todo_object = Todo.objects.create(user=user, ** validated_data)

        Item.objects.bulk_create([
            Item(todo=todo_object, **n) for n in item_data])

        return todo_object

    def update(self, instance, validated_data):
        items_data = validated_data.pop('todo')
        items = instance.todo.all()
        items = list(items)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        for new_item in items_data:
            old_item = items.pop(0)
            old_item.status = new_item.get('status', old_item.status)
            old_item.text = new_item.get('text', old_item.text)
            old_item.due_date = new_item.get('due_date', old_item.due_date)
            old_item.save()
        return instance