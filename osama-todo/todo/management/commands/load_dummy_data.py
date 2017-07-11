import random
import string
import calendar

from todo.models import TodoItem
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand


# UTILITY FUNCTIONS
def randomword(length):
    '''
    returns a random word of size 'length'
    '''
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


class Command(BaseCommand):
    def handle(self, **options):
        status_list = ['inprogress', 'pending', 'complete']

        for i in range(20):
            username = randomword(5)
            # password = 'arbisoft123'

            start_date = datetime.now().replace(day=1, month=1, year=2015).toordinal()
            end_date = datetime.now().toordinal()
            random_day = datetime.fromordinal(random.randint(start_date, end_date))
            random_day = timezone.make_aware(random_day)
            user = User.objects.create_user(
                username, password='arbisoft123',
                date_joined=random_day,
            )

            task_list = []
            for j in range(25):
                status = random.choice(status_list)
                #
                firstJan = timezone.make_aware(datetime.today().replace(day=1, month=1))
                days = abs((timezone.make_aware(datetime.now()) - firstJan).days)
                randomDay = firstJan + timedelta(days=random.randint(0, days))
                #
                if status == 'complete':
                    date_completed = randomDay
                else: 
                    date_completed = None

                task_list.append(TodoItem(
                    description=randomword(25),
                    status=status,
                    date_completed=date_completed,
                    user=user))
            TodoItem.objects.bulk_create(task_list)
