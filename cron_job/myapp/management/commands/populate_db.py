from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.admin import User
from myapp.models import DateTimeModel
import pytz


class Command(BaseCommand):
    help = "Creates users and timezone entries in the database"

    def handle(self, *args, **options):
        self.create_users()
        self.create_date_entries()

    def create_users(self):
        count = 1
        user_objects = []

        while count <= 5:
            user = self.dummy_user_credentials(count)
            user_objects.append(User(username=user['username'],
                                     password=user['password'], email=user['email'])
                                )
            count += 1

        User.objects.bulk_create(user_objects)
        self.stdout.write('Successfully created users')

    def dummy_user_credentials(self, count):
        user = {'username': 'user{num}'.format(num=count),
                'password': 'user{num}'.format(num=count),
                'email': 'user{num}@user.com'.format(num=count)}
        return user

    def create_date_entries(self):
        count = 1
        datetime_objects = []

        karachi_timezone = pytz.timezone('Asia/Karachi')
        new_datetime = timezone.now().astimezone(karachi_timezone)

        while count <= 15:
            datetime_objects.append(
                DateTimeModel(now=new_datetime.replace(tzinfo=None), 
                              timezone=karachi_timezone.zone)
            )
            count += 1

        DateTimeModel.objects.bulk_create(datetime_objects)
        self.stdout.write('Successfully created date entries')
