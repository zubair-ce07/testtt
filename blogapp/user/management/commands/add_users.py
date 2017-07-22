from django.core.management.base import BaseCommand
from csv import DictReader
from wblog.models import User


class Command(BaseCommand):
    help = 'Add bulk users from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    def handle(self, *args, **options):
        try:
            reader = DictReader(open(options['csv']))
            for record in reader:
                user = User(username=record['username'], email=record['email'])
                user.set_password(record['password'])
                user.info = record
                user.save()
        except IOError:
            self.stdout.write(self.style.SUCCESS('Cannot open "%s". Either file does not'
                                                 ' exist or it is a directory' % options['csv']))
