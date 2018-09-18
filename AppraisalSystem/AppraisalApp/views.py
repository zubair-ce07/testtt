from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, CompetencyForm
from django.views import generic
from .models import Employee, Feedback, Competency
from django.urls import reverse


class LoginView(generic.View):
    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'registration/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return redirect('appraisal:home')

        self.get(request)


class SignUpView(generic.View):
    def get(self, request):
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('appraisal:home')


@method_decorator(login_required, name='dispatch')
class Home(generic.TemplateView):
    template_name = 'profiles/home.html'


@method_decorator(login_required, name='dispatch')
class EmployeeView(generic.ListView):
    template_name = 'profiles/employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        user = self.request.user
        if user.employee_type == "CEO":
            employees = Employee.objects.exclude(pk=user.id)
        else:
            employees = Employee.objects.filter(reports_to=user)

        return employees


@method_decorator(login_required, name='dispatch')
class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'profiles/employee_details.html'
    context_object_name = 'employee'

    def get_object(self):
        employee_id = self.kwargs.get('pk')
        manager_id = self.request.user.id
        return Employee.get_record(employee_id, manager_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CompetencyForm()
        context['form'] = form
        return context


@method_decorator(login_required, name='dispatch')
class LogOutView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse('appraisal:login')


@method_decorator(login_required, name='dispatch')
class SendFeedbackView(generic.View):
    def post(self, request, emp_id):
        form = CompetencyForm(request.POST)
        if form.is_valid():
            from_user = request.user
            Competency.save_form(from_user, emp_id, form)

        return redirect('appraisal:employee_detail', pk=emp_id)


@method_decorator(login_required, name='dispatch')
class EditFeedbackView(generic.UpdateView):
    template_name = 'profiles/edit_feedback.html'
    model = Competency
    fields = ('comment', 'team_work', 'leadership')
    employee_id = 0

    def get_object(self):
        feedback_id = self.kwargs.get('feedback_id')
        competency = Competency.get_record(feedback_id)
        self.employee_id = Feedback.get_to_user_id(feedback_id)
        return competency

    def get_success_url(self):
        return reverse('appraisal:employee_detail', args=(self.employee_id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback_id'] = self.kwargs.get('feedback_id')
        return context


@method_decorator(login_required, name='dispatch')
class DeleteFeedbackView(generic.DeleteView):
    model = Feedback
    template_name = 'profiles/delete_feedback.html'
    employee_id = 0

    def get_object(self):
        feedback_id = self.kwargs.get('feedback_id')
        feedback_from = self.request.user
        self.employee_id = Feedback.get_to_user_id(feedback_id)
        return Feedback.get_record(feedback_id, feedback_from)

    def get_success_url(self):
        return reverse('appraisal:employee_detail', args=(self.employee_id,))


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(generic.UpdateView):
    template_name = 'profiles/edit_profile.html'
    model = Employee
    fields = ('first_name', 'last_name', 'address')

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('appraisal:home')
