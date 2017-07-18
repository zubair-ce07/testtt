from django.core.management.base import BaseCommand, CommandError
from csv import DictReader
from wblog.models import User


class Command(BaseCommand):
    help = 'Add bulk users from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    def handle(self, *args, **options):

        try:
            reader = DictReader(open(options['csv']))
            for csv_user in reader:
                user = User(username=csv_user['username'],
                            email=csv_user['email'],
                            password=csv_user['password']
                            )
                user.info = {'phone_num': csv_user['phone_num'],
                             'address': csv_user['address'],
                             'dob': csv_user['dob'],
                             'gender': csv_user['gender'],
                             'created_at': csv_user['created_at']
                             }
                user.save()
        except IOError:
            self.stdout.write(self.style.SUCCESS('Cannot open "%s". Either file does not'
                                                 ' exist or it is a directory' % options['csv']))
