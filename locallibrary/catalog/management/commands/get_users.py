from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Get users'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', dest='username', type=str, help='Username')

    def handle(self, *args, **kwargs):

        if kwargs['username']:
            try:
                users = User.objects.filter(username=kwargs['username'])
                for user in users:
                    output_string = 'Id: {}\nUsername: {}\nEmail: {}\nPasswword: {}'. \
                        format(user.id, user.username, user.email, user.password)
                    self.stdout.write(output_string)
            except User.DoesNotExist:
                self.stdout.write('User with username "%s" does not exist.' % kwargs['username'])
        else:
            users = User.objects.all()
            for user in users:
                output_string = 'Id: {}\nUsername: {}\nEmail: {}\nPasswword: {}'. \
                    format(user.id, user.username, user.email, user.password)
                self.stdout.write(output_string)
