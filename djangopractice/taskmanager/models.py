from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=Task)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = CustomUser.objects.get(pk=instance.assignee.id)
        message = 'A new task been assigned to you. Kindly review it by visiting ' \
                  'the website at http://127.0.0.1:8000/taskmanager/'
        send_mail('Task : '+instance.title, message, settings.EMAIL_HOST_USER, [user.email, ])


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
