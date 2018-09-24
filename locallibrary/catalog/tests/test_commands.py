from io import StringIO
from django.core.management import call_command
from django.test import TestCase

from catalog.models import Author


class GetAllAutohrsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_command_output(self):
        out = StringIO()
        call_command('get_allauthors', stdout=out)
        credentials = out.getvalue().split(' ')
        print(credentials)
        self.assertEquals('Big', credentials[2])
        self.assertEquals('Bob', credentials[5])
