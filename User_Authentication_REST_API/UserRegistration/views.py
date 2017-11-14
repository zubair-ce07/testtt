from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import (user_passes_test)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import (FormView, ListView, RedirectView, UpdateView,
                                  View)

from .forms import (AddTaskForm, AddUserTaskForm, CustomUserSignupForm,
                    LoginForm, UpdateProfileForm, UpdateTaskForm)
from .models import User, Task


class ProfileView(FormView):
    template_name = "UserRegistration/profile.html"

    form = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return render(request, self.template_name)
        else:
            return redirect('users:login')


class SignUpView(View):
    form = CustomUserSignupForm
    template_name = "UserRegistration/signup.html"

    def get(self, request):
        form = self.form(None)
        if request.user.is_authenticated:
            return redirect('users:profile')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            city = form.cleaned_data["city"]
            profile_picture = form.cleaned_data["profile_picture"]
            if User.objects.filter(email=email).exists():
                error = True
                return render(request, 'UserRegistration/signup.html', {'error': error, 'form': form})
            user = User.objects.create_user(username=username, email=email, password=password,
                                            first_name=first_name, last_name=last_name, city=city,
                                            profile_picture=profile_picture)
            return redirect('users:login')
        return render(request, 'UserRegistration/signup.html', {'form': form})


class LoginView(View):
    form = LoginForm
    template_name = "UserRegistration/login.html"

    def get(self, request):
        form = self.form(None)
        if request.user.is_authenticated:
            return redirect('users:profile')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user, created = User.objects.get_or_create(email=email, defaults={'username': 'User Name',
                                                                                    'first_name': 'First Name'})
            if created:
                user.set_password(password)
                user.save()
            user = authenticate(username=email, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('users:profile')
        error = True
        return render(request, self.template_name, {'form': form, 'error_fields': error})


class LogoutView(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        return reverse('users:login')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = UpdateProfileForm
    template_name = 'UserRegistration/edit_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(View):
    form = PasswordChangeForm
    template_name = "UserRegistration/change_password.html"

    def get(self, request):
        form = self.form(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('users:profile')
        error = True
        return render(request, self.template_name, {'form': form, 'error_fields': error})


class TasksView(ListView):
    template_name = 'UserRegistration/tasks.html'

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        if filter_val is None:
            return Task.objects.all()
        new_context = Task.objects.filter(name__icontains=filter_val)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                return render(request, self.template_name, {'tasks': Task.objects.all()})
            return render(request, self.template_name, {'tasks': Task.objects.filter(user=request.user.id)})
        else:
            error_not_login = True
            return render(request, "UserRegistration/login.html",
                          {'error_not_login': error_not_login, 'form': LoginForm})


class DeleteTaskView(RedirectView):
    template_name = 'UserRegistration/tasks.html'

    def get(self, request, *args, **kwargs):
        name = request.GET.get('task_name')
        Task.objects.filter(name=name).delete()
        if request.user.is_superuser:
            return render(request, self.template_name, {'tasks': Task.objects.all()})
        return render(request, self.template_name, {'tasks': Task.objects.filter(user=request.user.id)})


class UpdateTaskView(View):
    form = UpdateTaskForm
    template_name = "UserRegistration/edit_task.html"
    success_url = 'UserRegistration/tasks.html'

    def get(self, request):
        form = self.form(initial={'status': Task.objects.get(name=request.GET.get('task_name')).status})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            status = form.cleaned_data["status"]
            name = request.GET.get('task_name')
            Task.objects.filter(name=name).update(status=status)
            if request.user.is_superuser:
                return render(request, self.success_url, {'tasks': Task.objects.all()})
        return render(request, self.success_url, {'tasks': Task.objects.filter(user=request.user.id)})


class ShowAllTasksView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "UserRegistration/show_all_task.html"

    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        if filter_val is None:
            return Task.objects.all()
        new_context = Task.objects.filter(name__icontains=filter_val)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(ShowAllTasksView, self).get_context_data(**kwargs)
        return context


class AddNewTaskView(View):
    form = AddTaskForm
    template_name = "UserRegistration/add_task.html"

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(AddNewTaskView, self).dispatch(request,*args, **kwargs)

    def get(self, request):
        form = self.form(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            user = form.cleaned_data["user"]
            name = form.cleaned_data["name"]
            dated = form.cleaned_data["dated"]
            status = form.cleaned_data["status"]
            Task.objects.create(user=user, name=name, dated=dated, status=status)
            return redirect('users:tasks')
        return render(request, 'UserRegistration/add_task.html', {'form': form})


class AddUserTaskView(View):
    form = AddUserTaskForm
    template_name = "UserRegistration/add_task.html"

    def get(self, request):
        form = self.form(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            dated = form.cleaned_data["dated"]
            status = form.cleaned_data["status"]
            Task.objects.create(user=user, name=name, dated=dated, status=status)
            return redirect('users:tasks')
        return render(request, 'UserRegistration/add_task.html', {'form': form})
