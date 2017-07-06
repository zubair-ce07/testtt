from django.core.management.base import BaseCommand, CommandError
from training.models import Assignment


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('assignment_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for assignment_id in options['assignment_id']:
            try:
                assignment = Assignment.objects.get(pk=assignment_id)
            except Assignment.DoesNotExist:
                raise CommandError('Assignment "%s" does not exist' % assignment_id)

            assignment.completion_status = True
            assignment.save()

            print self.style.SUCCESS('Successfully Assignment'
                                     ':%s status changed' % assignment_id)
