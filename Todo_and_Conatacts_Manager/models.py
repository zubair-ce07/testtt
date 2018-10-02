from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


STATUS_CHOICES = (
        ("pending", 'Pending'),
        ('done', 'Done'),
        ('in-progress', 'In Progress'),
    )


class User(AbstractUser):
    phone_number = models.CharField(max_length=11)
    country = CountryField()
    profile_picture = models.URLField()


class TodoManager(models.Manager):
    def for_user(self, user):
        return super().get_queryset().filter(user=user)


class Todo(models.Model):
    objects = TodoManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user')
    title = models.CharField(max_length=50)


class Item(models.Model):
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending")
    text = models.CharField(max_length=50)
    due_date = models.DateTimeField()
    todo = models.ForeignKey(
        Todo, on_delete=models.CASCADE, related_name='todo')


class ContactManager(models.Manager):
    def for_user(self, user):
        return super().get_queryset().filter(user=user)


class Contact(models.Model):
    objects = ContactManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)
    country = models.CharField(max_length=30)
    profile_picture = models.URLField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'phone_number',)


@receiver(post_save, sender=User)
def notification(sender, instance, **kwargs):
    print("New user was added  or updated successfully.")
