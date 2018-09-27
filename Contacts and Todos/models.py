from django.db import models
from django.contrib.auth.models import AbstractUser

STATUS_CHOICES = [('DONE', 'Done'), ('IN_PROGRESS', 'In Progress'), ('NOT_STARTED', 'Not Started')]


class User(AbstractUser):
    phone_number = models.IntegerField(blank=True, null=True)
    profile_img = models.URLField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    country = models.CharField(max_length=20, blank=True, null=True)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    profile_img = models.URLField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False, null=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, blank=False, null=False, default='NOT_STARTED')


class Item(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    text = models.TextField(max_length=300, blank=False, null=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, blank=False, null=False, default='NOT_STARTED')
    due_date = models.DateField(blank=False, null=False)

    def get_items(user, todo_id):
        todo = Todo.objects.filter(id=todo_id, user=user)
        return Item.objects.filter(todo=todo[0]) if todo else []

