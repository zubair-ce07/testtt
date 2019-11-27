import  logging
from django.core.management.base import BaseCommand, CommandError
from mynotes.models import Note

# Setting logging level to Debug. By default the logging level is set to Warning.
logging.basicConfig(filename='login_middleware.log', level=logging.DEBUG)


class Command(BaseCommand):
    """Management Command to mark all notes in book as public"""
    help = 'Mark all notes of note book as public'

    def add_arguments(self, parser):
        parser.add_argument('book_id', type=int)

    def handle(self, *args, **options):
        book_id = options['book_id']
        try:
            notes = Note.objects.get(note_book_id=book_id).all()
        except Note.DoesNotExist:
            raise CommandError(f'Notes of this book_id = "{book_id}" does not exist')

        for note in notes:
            if not note.is_public:
                note.is_public = True
                note.save()

        logging.debug(f'Successfully marked add notes public for book_id = "{book_id}"')
