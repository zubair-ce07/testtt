from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime, timedelta


class Task(models.Model):
    title = models.CharField(max_length=50)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    due_date = models.DateField('Due Date',
                                default=datetime.now()+timedelta(days=7))
    status = models.BooleanField('Mark as Completed', default=False)

    def __str__(self):
        return "Title :" + self.title


def upload(instance, filename):
    filename += str(instance.id)
    return "media/" + filename


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    birth_date = models.DateField('Date of Birth', null=True)
    image = models.ImageField(upload_to=upload, default='media/profile.jpg')

    def total_tasks(self):
        return self.task_set.count()

    def full_name(self):
        return self.get_full_name()
