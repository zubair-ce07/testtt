import datetime
from django.core.management import call_command
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from taskmanager import tasks
from taskmanager.models import CustomUser, Task, DateTime

email_signal = Signal(providing_args=["password", "instance", "created"])

update_times_job_signal = Signal(providing_args=[])


def send_email(user, created, password):
    email_signal.send(sender=CustomUser, password=password, instance=user, created=created)


def send_update_time_signal():
    update_times_job_signal.send(sender=DateTime)


@receiver(email_signal, sender=CustomUser)
def send_registration_confirmation_mail(sender, instance, created, password, **kwargs):
    if created:
        tasks.send_email.delay(
            subject='Account creation',
            message=f"A new account has been created against your email. Login with the following password: {password}",
            recipients=[instance.email]
        )


@receiver(post_save, sender=Task)
def send_task_creation_mail(sender, instance, created, **kwargs):
    if created:
        datetime_object = datetime.datetime.strptime(str(instance.due_date), '%Y-%m-%d')
        tasks.send_email.delay(
            subject='Task Assignment',
            message=f"A new task {instance.title} has been assigned to you due on "
                    f"{datetime_object.strftime('%d, %B %Y')} by {instance.assigned_by.username} ",
            recipients=[instance.assignee.email])


@receiver(update_times_job_signal, sender=DateTime)
def start_update_time_cron_job(sender, **kwargs):
    call_command('crontab', 'add')
