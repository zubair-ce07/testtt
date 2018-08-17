import csv
import argparse

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.db import IntegrityError

from taskmanager import models


class Command(BaseCommand):
    help = "Add users in database from given CSV file. File format: username, email, password"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=argparse.FileType('r'))

    def handle(self, *args, **options):
        reader = csv.reader(options['file'])
        for username, email, password in reader:
            try:
                validate_email(email)
            except ValidationError:
                self.stdout.write('Error: Email Address is invalid for user ' + username)
            try:
                user = models.CustomUser(username=username, email=email, password=password)
                user.save()
            except IntegrityError:
                self.stdout.write('Error: username "' + username + '" already exists ')