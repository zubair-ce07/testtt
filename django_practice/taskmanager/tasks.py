from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail


# ./manage.py celeryd --loglevel=INFO

@shared_task
def send_email(recipients, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email='taskmanager.arbisoft@gmail.com',
        recipient_list=recipients,
    )
