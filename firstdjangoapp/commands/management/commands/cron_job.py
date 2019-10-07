from datetime import timedelta

from django.core.management.base import BaseCommand

from commands.models import DateTime


class Command(BaseCommand):
    help = 'Create random users'

    def handle(self, *args, **kwargs):
        if DateTime.objects.all()[0].time_zone == "PST" and DateTime.objects.filter(time_zone='UTC').count() > 0:
            pst_datetime = DateTime.objects.filter(time_zone='UTC')[:10]
            for date_time in pst_datetime:
                date_time.time_zone = 'PST'
                date_time.date_and_time = date_time.date_and_time + timedelta(hours=5)
                date_time.save()
        elif DateTime.objects.all()[0].time_zone == "PST" and DateTime.objects.filter(time_zone='UTC').count() == 0:
            pst_datetime = DateTime.objects.filter(time_zone='PST')[:10]
            for date_time in pst_datetime:
                date_time.time_zone = 'UTC'
                date_time.date_and_time = date_time.date_and_time - timedelta(hours=5)
                date_time.save()
        elif DateTime.objects.all()[0].time_zone == "UTC" and DateTime.objects.filter(time_zone='PST').count() > 0:
            pst_datetime = DateTime.objects.filter(time_zone='PST')[:10]
            for date_time in pst_datetime:
                date_time.time_zone = 'UTC'
                date_time.date_and_time = date_time.date_and_time - timedelta(hours=5)
                date_time.save()
        elif DateTime.objects.all()[0].time_zone == "UTC" and DateTime.objects.filter(time_zone='PST').count() == 0:
            pst_datetime = DateTime.objects.filter(time_zone='UTC')[:10]
            for date_time in pst_datetime:
                date_time.time_zone = 'PST'
                date_time.date_and_time = date_time.date_and_time + timedelta(hours=5)
                date_time.save()
