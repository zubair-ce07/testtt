from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from taskmanager import models


@receiver(post_save, sender=models.CustomUser)
def new_user(sender, instance, created, **kwargs):
    if created:
        message = 'Your new account has been set up. \n' \
                  'Visit Task Manager Profile : http://127.0.0.1:8000/taskmanager/{}/profile'
        user = models.CustomUser.objects.get(pk=instance.id)
        send_mail('Task Manager : New Account', message.format(user.id), settings.EMAIL_HOST_USER, [user.email, ])

@receiver(post_save, sender=models.Task)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = models.CustomUser.objects.get(pk=instance.assignee.id)
        message = 'A new task been assigned to you. Kindly review it by visiting ' \
                  'the website at http://127.0.0.1:8000/taskmanager/'
        send_mail('Task : '+instance.title, message, settings.EMAIL_HOST_USER, [user.email, ])

