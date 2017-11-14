from django.core.management.base import BaseCommand, CommandError
from memoapp.models import Activity
from datetime import datetime, timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        numbers = Activity.objects.filter(datetime__lt=datetime.today()-timedelta(days=1,hours=0,minutes=0,seconds=0)).delete()
        self.stdout.write(self.style.SUCCESS('Activites Removed Succesfully'+str(datetime.today()-timedelta(days=1,hours=0,minutes=0,seconds=0))))
