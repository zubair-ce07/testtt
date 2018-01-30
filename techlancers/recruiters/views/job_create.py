from django.views.generic import CreateView
from recruiters.models.job import Job


class JobCreateView(CreateView):
    fields = '__all__'
    model = Job
    template_name = "user/recruiter/post_job.html"
    success_url = "/"
