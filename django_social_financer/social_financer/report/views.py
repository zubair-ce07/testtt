from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect

from .forms import ReportForm
from .models import Report
from accounts.models import UserProfile

# Create your views here.
class ReportView(generic.FormView):
    template_name = 'report/file_report.html'
    form_class = ReportForm
    context_object_name = 'form'

    def form_valid(self, form):
        new_Report = Report()
        pair_user = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        new_Report.reported_user = pair_user
        new_Report.reporting_user = self.request.user.userprofile
        new_Report.category = form.cleaned_data['category']
        new_Report.comments = form.cleaned_data['comments']
        new_Report.save()
        return super(ReportView, self).form_valid(form)

    def get_success_url(self):
        pair_user = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        return reverse(self.get_reverse_url(pair_user.role))

    def get_reverse_url(self, role):
        return 'accounts:my_consumers' if role == 'DN' else 'accounts:home'


class ViewReports(generic.TemplateView):
    template_name = 'report/view_reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(id=context['pk'])
        return context
