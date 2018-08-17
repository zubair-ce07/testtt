from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from datetime import date, timedelta

from taskmanager import models


class Command(BaseCommand):
    help = "Sends email notification to all assignees who are due to complete their task in two days."
    message = 'Your task : "{title}" is due in two days !!\n' \
              'http://127.0.0.1:8000/taskmanager/{id}/details'

    def handle(self, *args, **options):
        due_date = date.today() + timedelta(days=2)
        tasks = models.Task.objects.filter(due_date=due_date, status=False)
        for task in tasks:
            send_mail('Task Manager Notification', self.message.format(id=task.id, title=task.title),
                      settings.EMAIL_HOST_USER, [task.assignee.email, ])

        self.stdout.write(self.style.SUCCESS('Email has been sent to relevant users'))