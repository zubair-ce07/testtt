from django.conf import settings

import pytz

from time_format_con.models import DateTime


def convert_datetime():
    with open(settings.BASE_DIR + '/index', 'r') as file:
        index = int(file.readline())

    datetimes = DateTime.objects.all()[index: index + 10]

    print "----------------------------------------------"
    for datetime in datetimes:
        if datetime.date.tzinfo == pytz.UTC:
            print "From :" + str(datetime.date)
            print "Converting to PKT"
            datetime.date = datetime.date.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone('US/Pacific'))
            print "To :" + str(datetime.date)
        else:
            print "Converting to UTC"
            datetime.date = datetime.date.astimezone(pytz.UTC)

        datetime.save()

    with open(settings.BASE_DIR + '/index', 'w') as file:
        file.write(str((index+10) % len(DateTime.objects.all())))
