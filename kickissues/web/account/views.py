from braces.views import AnonymousRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    CreateView, TemplateView, UpdateView
)
from pygal.style import DarkStyle

from web.account.charts import NumberOfIssueChart, TopManagersChart, YearlyIssueChart
from web.account.forms import UserForm, UserRegistrationForm
from web.account.utils import is_manager, is_manager_admin
from web.issue.models import Issue, StatusChoices


class RegisterView(AnonymousRequiredMixin, CreateView):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm
    authenticated_redirect_url = "account:dashboard"
    success_url = '/'


class CustomerRegisterView(RegisterView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actionurl"] = 'account:customer_register'
        return context

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='Customer')
        user.groups.add(group)
        login(self.request, user)
        return super().form_valid(form)


class ManagerRegisterView(RegisterView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actionurl"] = 'account:manager_register'
        return context

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='Manager')
        user.groups.add(group)
        return super().form_valid(form)


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
            context['todo'] = Issue.objects.filter(manage_by__isnull=True).order_by('created_at')
        elif is_manager_admin(self.request.user):
            context['manageradmin'] = True
            context['todo'] = Issue.objects.filter(status=StatusChoices.TODO)
            context['review'] = Issue.objects.filter(status=StatusChoices.REVIEW)
            context['resolved'] = Issue.objects.filter(status=StatusChoices.RESOLVED)
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
        if is_manager_admin(request.user):
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
        else:
            args = {
                "manageradmin": False
            }
        return render(request, 'account/stats.html', args)
