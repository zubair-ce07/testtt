import datetime
from django.core.management.base import BaseCommand
from taskmanager.models import Task
from taskmanager.tasks import send_email


class Command(BaseCommand):
    help = 'Takes a CSV file containing users information and enters them into database'

    def handle(self, *args, **options):
        current_date = datetime.date.today()
        due_date_to_check = current_date + datetime.timedelta(2)
        due_tasks = Task.objects.filter(due_date__range=[current_date, due_date_to_check])
        for task in due_tasks:
            send_email.delay(
                subject='Task reminder',
                message='A task assigned to you by {} is due this week on {}.'.format(task.assigned_by.get_full_name(),
                                                                                      task.due_date.strftime(
                                                                                          '%d %B, %Y')),
                recipients=[task.assignee.email])
            send_email.delay(
                subject='Task reminder',
                message='A task assigned by you to {} is due this week on {}.'.format(task.assignee.get_full_name(),
                                                                                      task.due_date.strftime(
                                                                                          '%d %B, %Y')),
                recipients=[task.assigned_by.email])
        self.stdout.write(self.style.SUCCESS('Due emails will be sent soon'))
