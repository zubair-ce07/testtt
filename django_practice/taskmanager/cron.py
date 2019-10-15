from datetime import timezone, timedelta

from taskmanager.models import DateTime


def generate_updated_times(timezone_offset, date_times):
    return [DateTime(id=date_time.id, datetime_str=date_time.datetime_str.astimezone(timezone(timedelta(hours=0))),
                     timezone_offset=timezone_offset) for date_time in date_times]


def update_times():
    date_times = DateTime.objects.filter(timezone_offset=5)[:10]
    if date_times:
        updated_date_times = generate_updated_times(timezone_offset=0, date_times=date_times)
    else:
        date_times = DateTime.objects.filter(timezone_offset=0)[:10]
        updated_date_times = generate_updated_times(timezone_offset=0, date_times=date_times)
    DateTime.objects.bulk_update(updated_date_times, fields=('datetime_str', 'timezone_offset'))
