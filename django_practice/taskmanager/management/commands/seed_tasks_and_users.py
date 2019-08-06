import json
import random
import string

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from taskmanager.models import CustomUser, Task
from taskmanager.signals import send_email


class NoArgumentException(Exception):
    """Raised if no argument is passed"""
    pass


class InvalidFilePathException(Exception):
    """Raised if no argument is passed"""
    pass


class Command(BaseCommand):
    help = 'Takes a json file containing tasks information and enters them into database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def randomString(self, string_length=10):
        """Generate a random string of fixed length """
        alphanumeric_characters = string.ascii_letters + string.digits
        return ''.join(random.choice(alphanumeric_characters) for i in range(string_length))

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            filepath = options.get('file')
            if not filepath:  # if no argument is passed
                raise NoArgumentException('argument can not be empty')
            if not filepath.endswith('.json'):
                raise InvalidFilePathException('invalid file type')
        except NoArgumentException:
            self.stdout.write("No argument is passed. Please pass a valid argument")
        except InvalidFilePathException:
            self.stdout.write(
                "Path was incorrect or does not lead to a json file. Please provide a valid json file path")
        except FileNotFoundError:
            self.stdout.write('File was not found at the given path. Please provide a valid path')
        else:
            with open(filepath) as file_cursor:
                json_reader = json.load(file_cursor)
                tasks_stats = {
                    'created': 0,
                    'updated': 0,
                    'failed': 0
                }
                users_stats = {
                    'created': 0,
                    'updated': 0,
                    'failed': 0
                }
                users = []
                for key, single_user_data in json_reader['users'].items():
                    # generate random alphanumeric password of length 10
                    password = self.randomString(10)
                    single_user_data['password'] = make_password(password)

                    try:
                        user, is_created = CustomUser.objects.get_or_create(
                            username=single_user_data.get('username'),
                            email=single_user_data.get('email'),
                            defaults=single_user_data)
                        users.append(user)
                        if is_created:
                            send_email(user, is_created, password)
                            users_stats['created'] += 1
                        else:
                            users_stats['updated'] += 1
                    except IntegrityError as dbError:
                        users_stats['failed'] += 1
                        self.stdout.write(
                            'user creation for user {} failed due to integrity errors'.format(str(single_user_data)))
                        self.stdout.write('Error: {}'.format(dbError))
                        self.stdout.write('')
                    except ValidationError as dbError:
                        users_stats['failed'] += 1
                        self.stdout.write(
                            'user creation for user {} failed due to validation errors'.format(str(single_user_data)))
                        self.stdout.write('Error: {}'.format(dbError))
                        self.stdout.write('')

                for key, single_task_data in json_reader['tasks'].items():
                    random.seed(random.randint)
                    single_task_data['assignee'] = random.choice(users)
                    single_task_data['assigned_by'] = random.choice(users)
                    try:
                        task, is_created = Task.objects.update_or_create(**single_task_data)
                        if is_created:
                            tasks_stats['created'] += 1
                        else:
                            tasks_stats['updated'] += 1
                    except ValidationError as dbError:
                        tasks_stats['failed'] += 1
                        self.stdout.write(
                            'task creation for task {}  failed due to database errors'.format(str(single_task_data)))
                        self.stdout.write('Error: {}'.format(dbError))
                        self.stdout.write('')

                self.stdout.write('Users seed stats')
                self.stdout.write('users created: {}'.format(users_stats['created']))
                self.stdout.write('users updated: {}'.format(users_stats['updated']))
                self.stdout.write('users failed: {}'.format(users_stats['failed']))
                self.stdout.write('')
                self.stdout.write('Tasks seed stats')
                self.stdout.write('tasks created: {}'.format(tasks_stats['created']))
                self.stdout.write('tasks updated: {}'.format(tasks_stats['updated']))
                self.stdout.write('tasks failed: {}'.format(tasks_stats['failed']))
