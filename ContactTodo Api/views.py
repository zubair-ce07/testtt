from rest_framework import viewsets

from ContactTodoManagement.models import User, Todo, Contact, Item

from .serializers import ContactSerializer, UserSerializer, ItemSerializer, TodoSerializer
from .permissions import can_add_contact, can_add_item, is_logged_in


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class ContactViewset(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [is_logged_in, can_add_contact]

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user=user)


class TodoViewset(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [is_logged_in]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


class ItemViewset(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [is_logged_in, can_add_item]

    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user)
        return Item.objects.filter(todo__in=todos)

