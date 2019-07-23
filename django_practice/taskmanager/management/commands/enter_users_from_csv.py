import csv
from django.core.management.base import BaseCommand
from taskmanager.models import CustomUser


class Command(BaseCommand):
    help = 'Takes a CSV file containing users information and enters them into database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def handle(self, *args, **options):
        with open(options['file']) as file_cursor:
            csv_reader = csv.reader(file_cursor, delimiter=',')
            next(csv_reader)
            for user_args in csv_reader:
                user = {
                    'first_name': user_args[0],
                    'last_name': user_args[1],
                    'email': user_args[2],
                    'username': user_args[3],
                    'address': user_args[4],
                    'birthday': user_args[5],
                    'profile_picture': user_args[7],
                }
                user_created = CustomUser.objects.create(**user)
                if user_created:
                    user_created.set_password(user_args[6])
                    user_created.save()

            self.stdout.write(self.style.SUCCESS('Successfully created users'))
