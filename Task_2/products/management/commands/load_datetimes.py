import csv
import datetime

from django.core.cache import cache
from django.core.management.base import BaseCommand
from pytz import timezone

from products.models import DateTime


class Command(BaseCommand):
    def handle(self, **options):
        cache.set('count', 0)
        cache.set('convert', True)
        date_time = datetime.datetime.now()
        time_zone = timezone('Asia/Karachi')
        date_time = time_zone.normalize(time_zone.localize(date_time))
        datetime_list = []
        for i in range(100):
            datetime_list.append(DateTime(datetime=date_time, timezone=time_zone.zone))
        DateTime.objects.bulk_create(datetime_list)
