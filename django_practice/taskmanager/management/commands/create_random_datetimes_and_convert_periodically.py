from datetime import datetime, timedelta, timezone
from random import random

from django.core.management.base import BaseCommand
from taskmanager.models import DateTime
from taskmanager.signals import send_update_time_signal


class Command(BaseCommand):
    help = 'generates 100 random datetimes in UTC, stores them in a database and starts a scheduled job that converts ' \
           'UTC to PST and vice versa '

    def handle(self, *args, **options):
        start_date_utc = datetime(1960, 1, 1).astimezone(timezone(timedelta(hours=5)))
        current_date = datetime.today().astimezone(timezone(timedelta(hours=5)))
        days_between_current_start = (current_date - start_date_utc).days
        random_datetimes = [
            DateTime(datetime_str=start_date_utc + (random() * timedelta(days=days_between_current_start)),
                     timezone_offset=5) for _ in range(100)]
        DateTime.objects.bulk_create(random_datetimes)
        send_update_time_signal()
