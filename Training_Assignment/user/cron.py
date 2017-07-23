from pytz import timezone, utc

from django.core.cache import cache

from task2.settings import TIME_ZONE
from user.models import DateTime


def time_zone_convert():
    tz = timezone(TIME_ZONE)
    count = cache.get('count')
    cache.set('count', count + 10)
    convert = cache.get('convert')
    if count >= DateTime.objects.count() - 10:
        cache.set('count', 0)
        cache.set('convert', not convert)
    if convert:
        for i in range(count, count + 10):
            date = DateTime.objects.all().order_by('id').__getitem__(i)
            dt = date.datetime
            dtz = tz.normalize(tz.localize(dt))
            dtz = dtz.astimezone(utc)
            dtz = dtz.replace(tzinfo=None)
            date.datetime = dtz
            date.timezone = utc.zone
            date.save()
    else:
        for i in range(count, count + 10):
            date = DateTime.objects.all().order_by('id').__getitem__(i)
            dt = date.datetime
            dtz = utc.localize(dt)
            dtz = dtz.astimezone(tz)
            dtz = dtz.replace(tzinfo=None)
            date.datetime = dtz
            date.timezone = tz.zone
            date.save()
