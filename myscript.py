'''
Script to bulk create 20 random users and randomly assign 500 tasks to them
'''
import random
import string
import calendar

from todo.models import TodoItem
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# UTILITY FUNCTIONS
def randomword(length):
    '''
    returns a random word of size 'length'
    '''
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


status_list = ['inprogress', 'pending', 'complete']

for i in range(20):
    username = randomword(5)
    # password = 'arbisoft123'
    user = User.objects.create_user(
        username, password='arbisoft123'
    )

    task_list = []
    for j in range(25):
        status = random.choice(status_list)
        #
        firstJan = datetime.today().replace(day=1, month=1)
        days = abs((datetime.now() - firstJan).days)
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
