from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.admin import User
from myapp.models import DateTimeModel
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):

    help = 'Converts the date from PST to UTC & vice versa'

    def handle(self, *args, **options):
        new_tz = pytz.timezone('America/Los_Angeles')
        objs = DateTimeModel.objects.all()

        for object in objs:

            if object.timezone == 'America/Los_Angeles':
                new_dt = object.now.replace(tzinfo=new_tz)
                new_dt = new_dt.astimezone(pytz.utc)

                DateTimeModel.objects.filter(pk=object.pk).update(now=new_dt, timezone='UTC')

            elif object.timezone == 'UTC':
                new_dt = object.now.replace(tzinfo=pytz.utc)
                new_dt = new_dt.astimezone(new_tz)

                DateTimeModel.objects.filter(pk=object.pk).update(
                    now=new_dt.replace(tzinfo=None),
                    timezone='America/Los_Angeles')
