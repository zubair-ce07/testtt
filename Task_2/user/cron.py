from pytz import timezone, utc

from django.core.cache import cache

from task2.settings import TIME_ZONE
from user.models import DateTime


def time_zone_convert():
    time_zone = timezone(TIME_ZONE)
    count = cache.get('count')
    cache.set('count', count + 10)
    convert = cache.get('convert')
    if count >= DateTime.objects.count() - 10:
        cache.set('count', 0)
        cache.set('convert', not convert)
    if convert:
        for i in range(count, count + 10):
            date = DateTime.objects.all().order_by('id').__getitem__(i)
            date_time = date.datetime
            date_time = time_zone.normalize(time_zone.localize(date_time))
            date_time = date_time.astimezone(utc)
            date_time = date_time.replace(tzinfo=None)
            date.datetime = date_time
            date.timezone = utc.zone
            date.save()
    else:
        for i in range(count, count + 10):
            date = DateTime.objects.all().order_by('id').__getitem__(i)
            date_time = date.datetime
            date_time = utc.localize(date_time)
            date_time = date_time.astimezone(time_zone)
            date_time = date_time.replace(tzinfo=None)
            date.datetime = date_time
            date.timezone = time_zone.zone
            date.save()
