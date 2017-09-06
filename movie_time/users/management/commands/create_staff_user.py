from __future__ import unicode_literals
import getpass
import sys
from django.contrib.auth import get_user_model
from django.core import exceptions
from django.core.management.base import BaseCommand
from django.utils.encoding import force_str


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.UserModel = get_user_model()
        self.email_field = self.UserModel._meta.get_field('email')
        self.moderator_field = self.UserModel._meta.get_field('is_moderator')
        self.admin_field = self.UserModel._meta.get_field('is_admin')

    def handle(self, *args, **options):
        email = None
        password = None

        try:
            while email is None:
                email = self.get_input_data(self.email_field, 'Enter Email: ')
                if not email:
                    continue
                try:
                    self.UserModel.objects.get(email=email)
                except self.UserModel.DoesNotExist:
                    pass
                else:
                    self.stderr.write('Error: That email is already taken.')
                    email = None

            while password is None:
                password = getpass.getpass()
                password2 = getpass.getpass(force_str('Password (again): '))
                if password != password2:
                    self.stderr.write("Error: Your passwords didn't match.")
                    password = None
                    continue

                if password.strip() == '':
                    self.stderr.write("Error: Blank passwords aren't allowed.")
                    password = None
                    continue

            is_moderator = self.get_input_data(self.moderator_field, 'Is Moderator (False): ', False)
            is_admin = self.get_input_data(self.moderator_field, 'Is Admin (False): ', False)

        except KeyboardInterrupt:
            self.stderr.write("\nOperation cancelled.")
            sys.exit(1)

        self.UserModel.objects.create_staff_user(email, password, is_admin, is_moderator)
        self.stdout.write("User created successfully.")

    def get_input_data(self, field, message, default=None):
        """
        Override this method if you want to customize data inputs or
        validation exceptions.
        """
        raw_value = input(message)
        if default is not None and raw_value == '':
            raw_value = default
        try:
            val = field.clean(raw_value, None)
        except exceptions.ValidationError as e:
            self.stderr.write("Error: %s" % '; '.join(e.messages))
            val = None

        return val
