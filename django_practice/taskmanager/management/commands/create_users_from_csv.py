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
            if '.csv' not in filepath:
                raise InvalidFilePathException()
            with open(filepath) as file_cursor:
                csv_reader = csv.DictReader(file_cursor)
                stats = {
                    'created': 0,
                    'updated': 0,
                    'failed': 0
                }
                for single_user_data in csv_reader:
                    new_user = {
                        'first_name': single_user_data.get('first_name'),
                        'last_name': single_user_data.get('last_name'),
                        'email': single_user_data.get('email'),
                        'username': single_user_data['username'],
                        'address': single_user_data.get('address'),
                        'birthday': single_user_data.get('birthday'),
                        'profile_picture': single_user_data.get('profile_picture'),
                        'password': make_password(single_user_data.get('password'))
                    }
                    try:
                        user, is_created = CustomUser.objects.update_or_create(**new_user)
                        if is_created:
                            stats['created'] += 1
                        else:
                            stats['updated'] += 1
                    except IntegrityError as dbError:
                        stats['failed'] += 1
                        print('user creation for user', str(new_user), 'failed due to integrity errors')
                        print('Error:', dbError)
                        print()
                    except ValidationError as dbError:
                        stats['failed'] += 1
                        print('user creation for user', str(new_user), 'failed due to validation errors')
                        print('Error:', dbError)
                        print()

                print('users created:', stats['created'])
                print('users updated:', stats['updated'])
                print('users failed:', stats['failed'])

        except NoArgumentException:
            print("No argument is passed. Please pass a valid argument")
        except InvalidFilePathException:
            print("Path was incorrect or does not lead to a csv file. Please provide a valid csv file path")
        except FileNotFoundError:
            print('File was not found at the given path. Please provide a valid path')
