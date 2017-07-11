import csv
import logging

from django.core.management.base import BaseCommand

from feedbacks.models import Feedbacks, Department, Store


class Command(BaseCommand):
    help = 'Fills the database with the given feedback file'

    def add_arguments(self, parser):
        parser.add_argument('file_dir', type=str)

    def handle(self, *args, **options):
        file_dir = options['file_dir']
        feedbacks = self.get_feedbacks_from_file(file_dir)
        Feedbacks.objects.bulk_create(feedbacks)

    def get_feedbacks_from_file(self, file_dir):
        try:
            with open(file_dir, "r") as csv_file:
                feedback_file = csv.DictReader(csv_file)
                feedbacks = []
                for row in feedback_file:
                    nps = None if row["nps"] == "" else row["nps"]
                    st_lvl = None if row["satisfaction_level"] == "" else row["satisfaction_level"]
                    department = self.get_department(row["department"])
                    store = self.get_store(row["store"])
                    feedback = Feedbacks(created_at=row["created_at"], name=row["name"],
                                         cell_phone=row["cell_phone"], email=row["email"],
                                         age=row["age"], gender=row["gender"],
                                         comment=row["comment"], nps=nps,
                                         satisfaction_level=st_lvl, department=department,
                                         store=store
                                         )
                    feedbacks.append(feedback)
                return feedbacks
        except IOError:
            logger = logging.getLogger()
            logger.exception("File not found")

    def get_department(self, dept_name):
        if dept_name == "":
            dept_name = "blank"

        try:
            department = Department.objects.get(name=dept_name)
        except Department.DoesNotExist:
            department = Department(name=dept_name)
            department.save()

        return department

    def get_store(self, store_name):
        if store_name == "":
            store_name = "blank"

        try:
            store = Store.objects.get(name=store_name)
        except Store.DoesNotExist:
            store = Store(name=store_name)
            store.save()

        return store



