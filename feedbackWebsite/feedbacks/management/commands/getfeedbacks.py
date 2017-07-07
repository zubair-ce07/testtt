import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from feedbacks.models import Feedbacks


class Command(BaseCommand):
    help = 'Fill the feedbacks in the database'

    def add_arguments(self, parser):
        parser.add_argument('file_dir', type=str)

    def handle(self, *args, **options):
        file_dir = options['file_dir']
        feedbacks = []
        my_file = Path(file_dir)

        if my_file.is_file() is False:
            self.stdout.write(self.style.SUCCESS('File not found'))
            return

        with open(file_dir, "r") as csv_file:
            feedback_file = csv.DictReader(csv_file)
            for row in feedback_file:
                feedback = Feedbacks(created_at=row["created_at"], name=row["name"],
                                     cell_phone=row["cell_phone"], email=row["email"],
                                     age=row["age"], gender=row["gender"],
                                     store=row["store"], department=row["department"],
                                     comment=row["comment"], nps=row["nps"],
                                     satisfaction_level=row["satisfaction_level"]
                                     )
                feedbacks.append(feedback)
        Feedbacks.objects.bulk_create(feedbacks)
        self.stdout.write(self.style.SUCCESS('Successfully inserted feedbacks'))
