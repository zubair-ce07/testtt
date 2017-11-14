from django.core.management.base import BaseCommand, CommandError
from user_api.models import Designation


class Command(BaseCommand):
    def handle(self, *args, **options):
        for job_title in Designation.JOB_TITLES:
            if Designation.objects.filter(job_title=job_title[0]).exists():
                self.stdout.write('Already Exists {}.'.format(job_title[0]))
            else:
                designation = Designation.objects.create(job_title=job_title[0])
                self.stdout.write(self.style.SUCCESS('Successfully created {}.'.format(designation.job_title)))
