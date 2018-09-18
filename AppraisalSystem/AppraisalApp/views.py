from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, HttpResponse, Http404, get_object_or_404
from .forms import SignUpForm, LoginForm, CompetencyForm, EditProfile
from django.core.exceptions import ObjectDoesNotExist
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


class SignUp(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        if user:
            login(self.request, user)
        return super(SignUp, self).form_valid(form)

    def get_success_url(self):
        return reverse('appraisal:home')


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
        """Return the last five published questions."""
        user = self.request.user
        # If CEO
        if user.employee_type == 1:
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
        employee = self.model.objects.get(pk=self.kwargs['pk'])
        if employee.reports_to != self.request.user and self.request.user.employee_type != 1:
            raise Http404()
        return employee

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        form = CompetencyForm()
        context['form'] = form
        return context


@method_decorator(login_required, name='dispatch')
class LogOutView(generic.RedirectView):
    url = '/appraisal/login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return self.url


@method_decorator(login_required, name='dispatch')
class SendFeedbackView(generic.View):
    def post(self, request, emp_id):
        form = CompetencyForm(request.POST)
        if form.is_valid():
            feedback = Feedback()
            feedback.from_user = request.user
            feedback.to_user = Employee.objects.get(pk=emp_id)
            feedback.save()

            competency = Competency()
            competency.feedback = feedback
            competency.comment = form.cleaned_data.get('comment')
            competency.team_work = form.cleaned_data.get('team_work')
            competency.leadership = form.cleaned_data.get('leadership')
            competency.save()
        return redirect('appraisal:employee_detail', pk=emp_id)


class EditFeedbackView(generic.UpdateView):
    success_url = ''


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


@method_decorator(login_required, name='dispatch')
class DeleteFeedbackView(generic.DeleteView):
    model = Feedback
    emp_id = 0
    template_name = 'profiles/delete_feedback.html'

    def get_object(self, queryset=None):
        try:
            feedback = Feedback.objects.get(pk=self.kwargs['pk'])
            if feedback.from_user == self.request.user:
                self.emp_id = feedback.to_user.id
                return feedback
            else:
                return None
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    def get_success_url(self):
        return reverse('appraisal:employee_detail', args=(self.emp_id,))


class ProfileUpdateView(generic.UpdateView):
    form_class = EditProfile
    template_name = 'profiles/edit_profile.html'
    model = Employee

    def get_object(self):
        id_ = self.request.user.pk
        return get_object_or_404(Employee, pk=id_)

    def get_success_url(self):
        return reverse('appraisal:home')


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
