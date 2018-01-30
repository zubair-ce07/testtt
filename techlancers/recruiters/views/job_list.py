from recruiters.models.job import Job
from django.views.generic import ListView


class JobListView(ListView):
    model = Job
    template_name = "user/freelancer/jobs.html"
