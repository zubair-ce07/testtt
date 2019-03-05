from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

STATUS_CHOICES = [('DONE', 'Done'), ('IN_PROGRESS', 'In Progress'), ('NOT_STARTED', 'Not Started')]


class User(AbstractUser):
    phone_number = models.IntegerField(blank=True, null=True)
    profile_img = models.URLField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    country = models.CharField(max_length=20, blank=True, null=True)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Contacts')
    name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    profile_img = models.URLField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Todos')
    title = models.CharField(max_length=30, blank=False, null=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, blank=False, null=False, default='NOT_STARTED')

    def update_todo(self, data):
        self.title = data.get('title', self.title)
        self.status = data.get('status', self.status)
        self.save()


class Item(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='Items')
    text = models.TextField(max_length=300, blank=False, null=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, blank=False, null=False, default='NOT_STARTED')
    due_date = models.DateField(blank=False, null=False)

    def get_items(user, todo_id):
        todo = Todo.objects.filter(id=todo_id, user=user)
        return Item.objects.filter(todo=todo[0]) if todo else []

    def update_item(item, item_received):
        item.status = item_received.get('status', item.status)
        item.text = item_received.get('text', item.text)
        item.due_date = item_received.get('due_date', item.due_date)
        item.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
