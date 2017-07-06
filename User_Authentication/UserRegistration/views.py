from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import TemplateView, View, RedirectView, FormView, UpdateView
from .forms import LoginForm, CustomUserSignupForm, UpdateProfileForm, UpdateTaskForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.urlresolvers import reverse, reverse_lazy
from .models import CustomUser, Task


# Create your views here.
class ProfileView(FormView):
    template_name = "UserRegistration/profile.html"

    form = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return render(request, self.template_name)
        else:
            return redirect('users:login')


class HomePageView(TemplateView):
    template_name = "UserRegistration/home.html"


class SignUpView(View):
    form = CustomUserSignupForm
    template_name = "UserRegistration/signup.html"

    def get(self, request):
        form = self.form(None)
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
            if CustomUser.objects.filter(email=email).exists():
                error = True
                return render(request, 'UserRegistration/signup.html', {'error': error, 'form': form})
            user = CustomUser.objects.create_user(username=username, email=email, password=password,
                                                  first_name=first_name, last_name=last_name, city=city,
                                                  profile_picture=profile_picture)
            return redirect('users:login')
        return render(request, 'UserRegistration/signup.html', {'form': form})


class LoginView(View):
    form = LoginForm
    template_name = "UserRegistration/login.html"

    def get(self, request):
        form = self.form(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user, created = CustomUser.objects.get_or_create(email=email, defaults={'username': 'User Name',
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


class UpdateProfileView(UpdateView):
    form_class = UpdateProfileForm
    template_name = 'UserRegistration/edit_profile.html'
    success_url = reverse_lazy('users:profile')
    login_url = '/login/'

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


class TasksView(RedirectView):
    template_name = 'UserRegistration/tasks.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
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
        return render(request, self.template_name, {'tasks': Task.objects.filter(user=request.user.id)})


class UpdateTaskView(View):
    form = UpdateTaskForm
    template_name = "UserRegistration/edit_task.html"
    success_url = 'UserRegistration/tasks.html'

    def get(self, request):
        form = self.form(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            status = form.cleaned_data["status"]
            name = request.GET.get('task_name')
            Task.objects.filter(name=name).update(status=status)
        return render(request, self.success_url, {'tasks': Task.objects.filter(user=request.user.id)})
