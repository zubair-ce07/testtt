import csv

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import DatabaseError, IntegrityError, transaction
from taskmanager.models import CustomUser


class NoArgumentException(Exception):
    """Raised if no argument is passed"""
    pass


class InvalidFilePathException(Exception):
    """Raised if argument doesnt have path to a valid csv file"""
    pass


class Command(BaseCommand):
    help = 'Takes a CSV file containing users information and enters them into database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            filepath = options.get('file')
            if not filepath:  # if no argument is passed
                raise NoArgumentException()
            if not filepath.endswith('.csv'):
                raise InvalidFilePathException()

        except NoArgumentException:
            self.stdout.write("No argument is passed. Please pass a valid argument")
        except InvalidFilePathException:
            self.stdout.write("Path was incorrect or does not lead to a csv file. Please provide a valid csv file path")
        except FileNotFoundError:
            self.stdout.write('File was not found at the given path. Please provide a valid path')

        else:
            with open(filepath) as file_cursor:
                csv_reader = csv.DictReader(file_cursor)
                stats = {
                    'created': 0,
                    'updated': 0,
                    'failed': 0
                }
                for single_user_data in csv_reader:
                    single_user_data['password'] = make_password(single_user_data.get('password'))
                    try:
                        user, is_created = CustomUser.objects.update_or_create(**single_user_data)
                        if is_created:
                            stats['created'] += 1
                        else:
                            stats['updated'] += 1
                    except IntegrityError as dbError:
                        stats['failed'] += 1
                        self.stdout.write(
                            'user creation for user {} failed due to integrity errors'.format(single_user_data))
                        self.stdout.write('Error: {}'.format(dbError))
                        self.stdout.write('')
                    except ValidationError as dbError:
                        stats['failed'] += 1
                        self.stdout.write(
                            'user creation for user {} failed due to validations errors'.format(single_user_data))
                        self.stdout.write('Error: {}'.format(dbError))
                        self.stdout.write('')

                self.stdout.write('users created: {}'.format(stats['created']))
                self.stdout.write('users updated: {}'.format(stats['updated']))
                self.stdout.write('users failed: {}'.format(stats['failed']))
