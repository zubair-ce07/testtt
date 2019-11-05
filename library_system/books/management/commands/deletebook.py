"""Module for admin command for deleting book."""

from django.core.management.base import BaseCommand, CommandError
from books.models import Book

class Command(BaseCommand):
    """Class for deleting book from console."""

    help = 'creates new user'

    def add_arguments(self, parser):
        """Class for getting arguments from console."""
        parser.add_argument('title', nargs='?', type=str)

    def handle(self, *args, **kwargs):
        """Class for handling arguments from console."""
        try:
            book_title = kwargs['title']
            book = Book.objects.get(title=book_title)
            book.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted book "%s"' % book_title))     
        except book.DoesNotExist:
            raise CommandError('"%s" book does not exist in the database.' % book_title)
        except book.MultipleObjectsReturned:
            raise CommandError('Multiple books returned.')
