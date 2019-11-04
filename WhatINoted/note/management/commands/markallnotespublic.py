from django.core.management.base import BaseCommand, CommandError
from note.models import Note


class Command(BaseCommand):
    help = 'Mark all notes of note book as public'

    def add_arguments(self, parser):
        parser.add_argument('book_id', type=int)

    def handle(self, *args, **options):
        book_id = options['book_id']
        try:
            notes = Note.objects.filter(note_book_id=book_id)
        except Note.DoesNotExist:
            raise CommandError('Notes of this book_id = "%s" does not exist' % book_id)

        for note in notes:
            note.is_public = True
            note.save()

        self.stdout.write(self.style.SUCCESS('Successfully marked add notes public for book_id = "%s"' % book_id))
