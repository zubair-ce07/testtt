import datetime
from django.core.management.base import BaseCommand
from taskmanager.models import Task
from taskmanager.tasks import send_email


class Command(BaseCommand):
    help = 'Takes a CSV file containing users information and enters them into database'

    def handle(self, *args, **options):
        current_date = datetime.date.today()
        start_week = current_date - datetime.timedelta(current_date.weekday())
        end_week = start_week + datetime.timedelta(7)
        due_tasks = Task.objects.filter(due_date__range=[start_week, end_week])
        for task in due_tasks:
            send_email.delay(
                subject='Task reminder',
                message='A task assigned to you by {} is due this week on {}.'.format(task.assigned_by.get_full_name(),
                                                                                      task.due_date),
                recipients=[task.assignee.email])
            send_email.delay(
                subject='Task reminder',
                message='A task assigned by you to {} is due this week on {}.'.format(task.assignee.get_full_name(),
                                                                                      task.due_date),
                recipients=[task.assigned_by.email])
        self.stdout.write(self.style.SUCCESS('Due emails will be sent soon'))
