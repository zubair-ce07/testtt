
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, \
    logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.base import View
from system.utils import get_forms_context, save_forms, \
    redirect_to_home
from .forms import SignUpForm
from system.models import Appraisal


User = get_user_model()


"""-----------------------------------------Update and Add Appraisal"""


class AppraisalView(LoginRequiredMixin, View):
    template = "system/appraisal.html"

    def get(self, request, id=None):
        context = get_forms_context(request, id)
        return render(request, self.template, context)

    def post(self, request, id=None):
        context = get_forms_context(request, id)
        appraisal_form = context.get('appraisal_form')
        competence_form = context.get('competence_form')
        if appraisal_form.is_valid() and competence_form.is_valid():
            save_forms(appraisal_form, competence_form, id)
            return redirect_to_home(request)
        return render(request, self.template, context)


"""-----------------------------------------Delete Appraisal"""


class AppraisalDeleteView(LoginRequiredMixin, DeleteView):
    model = Appraisal
    template_name = 'system/appraisal-confirm-delete.html'
    success_url = reverse_lazy('view_employees')


"""-----------------------------------------------List views"""


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'system/view_employees.html'
    context_object_name = 'all_employees'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(report_to=self.request.user.id)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user_pk'] = self.request.user.id
        return data


class AppraisalListView(LoginRequiredMixin, generic.ListView):
    model = Appraisal
    context_object_name = 'all_apparaisal'
    template_name = "system/view-appraisals.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(to_user=self.kwargs.get('pk', 0))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['context'] = self.request.user.user_level
        return data


"""--------------------------------------------Login-signup-settings"""


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password is successfully updated!')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'form.html', {'form': form, 'context': "Save"})


def signupUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect_to_home(request)
    else:
        form = SignUpForm()
    return render(request, 'form.html', {'form': form, 'context': "Sign Up"})


def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_to_home(request)
    else:
        form = AuthenticationForm()
    return render(request, 'form.html', {'form': form, 'context': "Log In"})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')


"""------------------------------------------------------index"""


def index(request):
    if request.user.is_authenticated:
        return redirect_to_home(request)
    else:
        return render(request, 'form.html')
