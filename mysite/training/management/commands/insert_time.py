from django.core.management.base import BaseCommand, CommandError

from datetime import datetime

from training.models import DateTime

class Command(BaseCommand):
    help = 'Adds 100 datetimes to DateTime table'

    def handle(self, *args, **options):
        datetimes = [DateTime(date=datetime.now()) for i in range(0,100)]
        DateTime.objects.bulk_create(datetimes)