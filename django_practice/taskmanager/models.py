from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from taskmanager.tasks import send_email


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


@receiver(post_save, sender=CustomUser)
def send_registration_confirmation_mail(sender, instance, created, **kwargs):
    if created:
        send_email.delay(
            subject='Account creation',
            message='A new account has been created against your email.',
            recipients=[instance.email]
        )


@receiver(post_save, sender=Task)
def send_task_creation_mail(sender, instance, created, **kwargs):
    if created:
        send_email.delay(
            subject='Task Assignment',
            message='A new task ' + instance.title + ' has been assigned to you due on ' +
                    instance.due_date.strftime('%d, %B %Y'),
            recipients=[instance.assignee.email],
        )


post_save.connect(send_registration_confirmation_mail, sender=CustomUser)
post_save.connect(send_task_creation_mail, sender=Task)
