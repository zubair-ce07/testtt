from django.conf import settings

import pytz

from .models import DateTime


def my_scheduled_job():
    with open(settings.BASE_DIR + '/index', 'r') as file:
        index = int(file.readline())

    datetimes = DateTime.objects.all()[index: index+5]

    print "-------------------Running-------------------"
    for datetime in datetimes:
        if datetime.date.tzinfo == pytz.UTC:
            print "Converting to PKT"
            datetime.date = datetime.date.astimezone(pytz.timezone(
                'US/Pacific'))
        else:
            print "Converting to UTC"
            datetime.date = datetime.date.astimezone(pytz.UTC)

        datetime.save()

    with open(settings.BASE_DIR + '/index', 'w') as file:
        file.write(str((index+5) % len(DateTime.objects.all())))
