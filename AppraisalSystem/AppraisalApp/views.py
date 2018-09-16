from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, LoginForm, CompetencyForm
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


def home(request):
    return render(request, 'profiles/home.html', {'user': request.user})


class EmployeeView(generic.ListView):
    template_name = 'profiles/employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        """Return the last five published questions."""
        user = self.request.user

        # If CEO
        if user.employee_type == 1:
            employees = Employee.objects.all()

        else:
            employees = Employee.objects.filter(reports_to=user)

        return employees


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'profiles/employee_details.html'
    context_object_name = 'employee'


def employee_detail(request, uid):
    try:
        employee = Employee.objects.get(pk=uid)
    except:
        return HttpResponse("Employee not found")

    if employee.reports_to != request.user:
        return HttpResponse("Employee is not under your command")

    form = CompetencyForm()
    context = {}
    context['employee'] = employee
    context['form'] = form
    return render(request, 'profiles/employee_details.html', context)


def user_logout(request):
    logout(request)
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


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
