from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.contrib.auth.admin import User
from myapp.models import DateTimeModel
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = "Creates users and timezone entries in the database"

    def handle(self, *args, **options):
        #self.create_users()
        self.create_date_entries()

    def create_users(self):
        count = 1
        objs = []

        while count <= 5:
            user = self.get_user(count)
            objs.append(User(username=user['username'],
                             password=user['password'], email=user['email']
                             )
                        )
            count += 1

        User.objects.bulk_create(objs)
        self.stdout.write('Successfully created users')

    def get_user(self, count):
        user = {'username': 'user{num}'.format(num=count),
                'password': 'user{num}'.format(num=count),
                'email': 'user{num}@user.com'.format(num=count)}
        return user

    def create_date_entries(self):
        count = 1
        objs = []

        new_tz = pytz.timezone('Asia/Karachi')
        new_dt = timezone.now().astimezone(new_tz)
        new_dt.dst(is_dst=False)

        while count <= 15:
            objs.append(
                DateTimeModel(now=new_dt.replace(tzinfo=None), timezone='Asia/Karachi')
            )
            count += 1

        DateTimeModel.objects.bulk_create(objs)
        self.stdout.write('Successfully created date entries')
