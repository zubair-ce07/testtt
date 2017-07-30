from django.conf import settings
from django.core.cache import cache
from pytz import timezone, utc

from products.models import DateTime


def time_zone_convert():
    time_zone = timezone(settings.TIME_ZONE)
    count = cache.get('count')
    cache.set('count', count + 10)
    convert = cache.get('convert')
    if count >= DateTime.objects.count() - 10:
        cache.set('count', 0)
        cache.set('convert', not convert)
    datetimes = DateTime.objects.all()[count: count + 10]
    for date in datetimes:
        date_time = date.datetime
        if convert:
            date_time = time_zone.normalize(time_zone.localize(date_time))
            date_time = date_time.astimezone(utc)
        else:
            date_time = utc.localize(date_time)
            date_time = date_time.astimezone(time_zone)
        date_time = date_time.replace(tzinfo=None)
        date.datetime = date_time
        date.timezone = utc.zone
        date.save()
