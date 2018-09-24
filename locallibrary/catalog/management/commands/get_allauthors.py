from django.core.management.base import BaseCommand, CommandError
from catalog.models import Author
from django.db.models import Q


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--contain',
            dest='contain',
            help='Get those authors whose name contains this string',
        )

    def handle(self, *args, **options):
        # ...
        if options['contain']:
            authors = Author.objects.filter(
                Q(first_name__icontains=options['contain']) |
                Q(last_name__icontains=options['contain'])
            )
        else:
            authors = Author.objects.all()

        if not authors:
            self.stdout.write(self.style.SUCCESS('No author avaialbe'))
        for author in authors:
            self.stdout.write(self.style.SUCCESS(
                'First Name: {} Last Name: {} Date of Birth: {}'.format(author.first_name,
                                                                          author.last_name, author.date_of_birth)
            ))
