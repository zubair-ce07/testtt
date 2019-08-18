import json
import random
from string import ascii_letters, digits

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from taskmanager.models import CustomUser, Task
from taskmanager.signals import send_email


class Command(BaseCommand):
    help = 'Takes a json file containing tasks information and enters them into database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def print_stats(self, entity, stats):
        self.stdout.write(f'{entity} seed stats')
        self.stdout.write(f"{entity} created: {stats['created']}")
        self.stdout.write(f"{entity} updated: {stats['updated']}")
        self.stdout.write(f"{entity} failed: {stats['failed']}")
        self.stdout.write('')

    def print_error(self, entity, error_type, error, entity_details):
        self.stdout.write(
            f'{entity} creation for {entity} {str(entity_details)}  failed due to {error_type} errors')
        self.stdout.write(f'Error: {error}')
        self.stdout.write('')

    @transaction.atomic
    def handle(self, *args, **options):
        filepath = options.get('file')
        if not filepath:
            self.stdout.write('No argument is passed. Please pass a valid argument')
        elif not filepath.endswith('.json'):
            self.stdout.write(
                'Path was incorrect or does not lead to a json file. Please provide a valid json file path')
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
                for single_user_data in json_reader['users'].values():
                    print(single_user_data)
                    password = CustomUser.objects.make_random_password(length=10,
                                                                       allowed_chars=ascii_letters + digits)
                    single_user_data['password'] = make_password(password)

                    try:
                        user, is_created = CustomUser.objects.update_or_create(
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
                        self.print_error(entity='user', error_type='integrity', error=dbError,
                                         entity_details=single_user_data)
                    except ValidationError as dbError:
                        users_stats['failed'] += 1
                        self.print_error(entity='user', error_type='validation', error=dbError,
                                         entity_details=single_user_data)

                for single_task_data in json_reader['tasks'].values():
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
                        self.print_error(entity='task', error_type='validation', error=dbError,
                                         entity_details=single_task_data)

                self.print_stats('Users', users_stats)
                self.print_stats('Tasks', tasks_stats)
