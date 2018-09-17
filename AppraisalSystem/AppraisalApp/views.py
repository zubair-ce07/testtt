from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, LoginForm, CompetencyForm, EditProfile
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from .models import Employee, Feedback, Competency


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return redirect('appraisal:home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('appraisal:home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def home(request):
    return render(request, 'profiles/home.html', {'user': request.user})


@method_decorator(login_required, name='dispatch')
class EmployeeView(generic.ListView):
    template_name = 'profiles/employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        """Return the last five published questions."""
        user = self.request.user

        # If CEO
        if user.employee_type == 1:
            employees = Employee.objects.exclude(pk=user.id)

        else:
            employees = Employee.objects.filter(reports_to=user)

        return employees


@login_required
def employee_detail(request, uid):
    try:
        employee = Employee.objects.get(pk=uid)
    except ObjectDoesNotExist:
        return HttpResponse("Employee not found")

    if employee.reports_to != request.user and request.user.employee_type != 1:
        return HttpResponse("Employee is not under your command")

    form = CompetencyForm()
    context = {}
    context['employee'] = employee
    context['form'] = form
    return render(request, 'profiles/employee_details.html', context)


@login_required
def user_logout(request):
    logout(request)
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def send_feedback(request, uid):
    if request.method == "POST":
        form = CompetencyForm(request.POST)
        if form.is_valid():
            feedback = Feedback()
            feedback.from_user = request.user
            feedback.to_user = Employee.objects.get(pk=uid)
            feedback.save()

            competency = Competency()
            competency.feedback = feedback
            competency.comment = form.cleaned_data.get('comment')
            competency.team_work = form.cleaned_data.get('team_work')
            competency.leadership = form.cleaned_data.get('leadership')
            competency.save()

    return redirect('appraisal:employee_detail', uid=uid)


@login_required
def edit_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(pk=feedback_id)
        competency = Competency.objects.get(feedback=feedback)
    except ObjectDoesNotExist:
        return HttpResponse("Feedback Doesn't exists")

    if feedback.from_user == request.user:
        if request.method == "POST":
            form = CompetencyForm(request.POST)
            if form.is_valid():
                competency.comment = form.cleaned_data.get('comment')
                competency.leadership = form.cleaned_data.get('leadership')
                competency.team_work = form.cleaned_data.get('team_work')
                competency.save()
                return redirect('appraisal:employee_detail', uid=feedback.to_user.id)
        else:
            form_context = {}
            form_context['comment'] = competency.comment
            form_context['leadership'] = competency.leadership
            form_context['team_work'] = competency.team_work
            form = CompetencyForm(initial=form_context)
    else:
        return HttpResponse("Permission Denied")

    return render(request, 'profiles/edit_feedback.html', {'form': form, 'feedback_id': feedback_id})


@login_required
def delete_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(pk=feedback_id)
        if feedback.from_user == request.user:
            employee_id = feedback.to_user.id
            feedback.delete()
            return redirect('appraisal:employee_detail', uid=employee_id)
        else:
            return HttpResponse("Permission Denied")

    except ObjectDoesNotExist:
        return HttpResponse("Feedback not found")


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = EditProfile(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.address = form.cleaned_data.get('address')
            user.save()
        return render(request, 'profiles/home.html')
    else:
        form = EditProfile(
            initial={'first_name': user.first_name, 'last_name': user.last_name, 'address': user.address}
        )

    return render(request, 'profiles/edit_profile.html', {'form': form})
