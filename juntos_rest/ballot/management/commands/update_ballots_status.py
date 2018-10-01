from django.core.management.base import BaseCommand

from ballot.tasks import update_ballots_status


class Command(BaseCommand):
    """
    Run task update_ballots_status
    """
    help = "Run task update_ballots_status"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """Handles command"""
        try:
            update_ballots_status.delay()
        except:
            self.stdout.write(self.style.WARNING(
                "Couldn't run task."
            ))

        self.stdout.write(
            self.style.SUCCESS("Successfully run task to update ballots status.")
        )
