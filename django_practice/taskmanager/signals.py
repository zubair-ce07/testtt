import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from taskmanager.models import CustomUser, Task
from taskmanager import tasks

email_signal = Signal(providing_args=["password", "instance", "created"])


def send_email(user, created, password):
    email_signal.send(sender=CustomUser, password=password, instance=user, created=created)


@receiver(email_signal, sender=CustomUser)
def send_registration_confirmation_mail(sender, instance, created, password, **kwargs):
    if created:
        tasks.send_email.delay(
            subject='Account creation',
            message='A new account has been created against your email. Login with the following password: {}'.format(
                password),
            recipients=[instance.email]
        )


@receiver(post_save, sender=Task)
def send_task_creation_mail(sender, instance, created, **kwargs):
    if created:
        datetime_object = datetime.datetime.strptime(instance.due_date, '%Y-%m-%d')
        tasks.send_email.delay(
            subject='Task Assignment',
            message='A new task {} has been assigned to you due on {} by {}'.format(instance.title,
                                                                                    datetime_object.strftime(
                                                                                        '%d, %B %Y'),
                                                                                    instance.assigned_by.username
                                                                                    ),
            recipients=[instance.assignee.email])
