from django.core.management.base import BaseCommand
from myapp.models import DateTimeModel
import pytz


class Command(BaseCommand):
    help = 'Converts the datetime_object from PST to UTC & vice versa'

    def handle(self, *args, **options):
        karachi_timezone = pytz.timezone('Asia/Karachi')
        current_datetime_entries = DateTimeModel.objects.all()

        for datetime_object in current_datetime_entries:

            if datetime_object.timezone == karachi_timezone.zone:
                self.convert_time(datetime_object=datetime_object,
                                  current_timezone=karachi_timezone)

            elif datetime_object.timezone == pytz.utc.zone:
                self.convert_time(datetime_object=datetime_object,
                                  current_timezone=pytz.utc,
                                  new_timezone=karachi_timezone)

    def convert_time(self, datetime_object, current_timezone,
                     new_timezone=pytz.utc):

        new_datetime = datetime_object.now.replace(tzinfo=current_timezone)
        new_datetime = new_datetime.astimezone(new_timezone)

        datetime_object.now = new_datetime.replace(tzinfo=None)
        datetime_object.timezone = new_timezone.zone
        datetime_object.save()
