"""Module for admin command for creating book."""

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from books.models import Book


class Command(BaseCommand):
    """Class for creating new book from console."""

    help = 'creates new user'

    def add_arguments(self, parser):
        """Class for getting arguments from console."""
        parser.add_argument('title', nargs='+', type=str)
        parser.add_argument('author', nargs='+', type=str)
        parser.add_argument('number_of_books', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        """Class for handling arguments from console."""
        try:
            titles = kwargs['title']
            authors = kwargs['author']
            number_of_books = kwargs['number_of_books']
            for book_title in titles:
                title = book_title
            for book_author in authors:
                author = book_author
            for number_of_book in number_of_books:
                book_count = number_of_book
            book = Book(title=title, author_name=author, number_of_books=book_count)
            book.save()
            self.stdout.write(self.style.SUCCESS('Successfully created book "%s"' % title))
        except IntegrityError:
            raise CommandError('"%s" book already exists in the database.' % title)
