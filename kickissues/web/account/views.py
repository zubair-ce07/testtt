from braces.views import AnonymousRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView, TemplateView, UpdateView
)
from pygal.style import DarkStyle

from .charts import NumberOfIssueChart, TopManagersChart, YearlyIssueChart
from .forms import UserForm, UserRegistrationForm
from .utils import is_manager, is_manager_admin
from ..issue.models import Issue


class RegisterView(AnonymousRequiredMixin, CreateView):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm
    authenticated_redirect_url = "account:dashboard"
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.kwargs['type'] is None:
            redirect('account:usertype')
        context['type'] = self.kwargs['type']
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            usertype = request.POST.get("type")
            if usertype == 'manager':
                group = Group.objects.get(name='Manager')
            else:
                group = Group.objects.get(name='Customer')
            user.groups.add(group)
            login(request, user)
            return redirect('/')
        return render(request, 'account/register.html', {'form': form})


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'account/edit_profile.html'
    success_url = 'account:dashboard'
    form_class = UserForm
    model = User

    def get_success_url(self):
        return reverse('account:dashboard')


class UserType(AnonymousRequiredMixin, TemplateView):
    authenticated_redirect_url = "account:dashboard"
    template_name = 'account/usertype.html'


class UserDashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'account:login'
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if is_manager(self.request.user):
            context['manager'] = True
            context['manage_by'] = Issue.objects.filter(manage_by=self.request.user)
            context['todo'] = Issue.objects.filter(manage_by=None).order_by('date_created')
        elif is_manager_admin(self.request.user):
            context['manageradmin'] = True
            context['todo'] = Issue.objects.filter(status='todo')
            context['review'] = Issue.objects.filter(status='review')
            context['resolved'] = Issue.objects.filter(status='resolved')
        else:
            context['customer'] = True
            context['created_by'] = Issue.objects.filter(created_by=self.request.user)
        return context


class UserStatsView(LoginRequiredMixin, TemplateView):
    login_url = 'account:login'
    template_name = 'account/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if is_manager_admin(self.request.user):
            context['manageradmin'] = True
            context['manager_list'] = User.objects.filter(groups__name='Manager')
            top_manager_chart = TopManagersChart(
                height=600,
                width=800,
                explicit_size=True,
                style=DarkStyle,
            )
            context["top_manager_chart"] = top_manager_chart.generate()
        else:
            issue_chart = NumberOfIssueChart(
                height=600,
                width=600,
                explicit_size=True,
                style=DarkStyle,
                user=self.request.user
            )

            yearly_chart = YearlyIssueChart(
                height=600,
                width=800,
                explicit_size=True,
                style=DarkStyle,
                user=self.request.user
            )
            context['issue_chart'] = issue_chart.generate()
            context['yearly_chart'] = yearly_chart.generate()
        return context

    def post(self, request):
        manager_id = int(request.POST.get('manager'))
        manager_instance = User.objects.get(id=manager_id)

        issue_chart = NumberOfIssueChart(
            height=600,
            width=600,
            explicit_size=True,
            style=DarkStyle,
            user=manager_instance
        )

        yearly_chart = YearlyIssueChart(
            height=600,
            width=800,
            explicit_size=True,
            style=DarkStyle,
            user=manager_instance
        )

        top_manager_chart = TopManagersChart(
            height=600,
            width=800,
            explicit_size=True,
            style=DarkStyle,
        )

        args = {
            "manageradmin": True,
            "manager_list": User.objects.filter(groups__name='Manager'),
            "yearly_chart": yearly_chart.generate(),
            "top_manager_chart": top_manager_chart.generate(),
            "issue_chart": issue_chart.generate(),
            "selected_manager": manager_id
        }
        return render(request, 'account/stats.html', args)
