from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField('email address', blank=True, unique=True)
    address = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="images/avatars/", blank=True, null=True)


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignee')
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_by', null=True)
    due_date = models.DateField()
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(default='Pending', choices=(('pending', 'Pending'), ('complete', 'Complete'),),
                              max_length=10)


class DateTime(models.Model):
    datetime_str = models.DateTimeField()
    timezone_offset = models.IntegerField(default=5, choices=((0, '0'), (5, '5')),
                                          error_messages={'invalid_choice': 'value provided is not a invalid.', }, )
