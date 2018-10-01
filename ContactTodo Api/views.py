from rest_framework import viewsets
from django.shortcuts import Http404
from ContactTodoManagement.models import User, Todo, Contact, Item
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import ContactSerializer, UserSerializer, ItemSerializer, TodoSerializer
from .permissions import can_add_contact, can_add_item


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def update(self, request, *args, **kwargs):
        if request._user.id == kwargs.get('pk', 0):
            return super().update(request, *args, **kwargs)
        else:
            raise Http404("this user not found")


class ContactViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, can_add_contact]

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user=user)


class TodoViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


class ItemViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, can_add_item]

    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user)
        return Item.objects.filter(todo__in=todos)
