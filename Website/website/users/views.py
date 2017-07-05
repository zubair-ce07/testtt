from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import RedirectView, TemplateView, View
from django.views.generic.edit import UpdateView

from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm


class UserRegisterFormView (View):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('users:profile')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('users:login')
        return render(request, self.template_name, {'form': form})


class UserLoginFormView (View):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('users:profile')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'error': ' '})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        message = Message.LOGIN_DISABLED
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('users:profile')
            message = Message.LOGIN_INVALID
        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form, 'error': message})


class UserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'users/edit.html'
    success_url = reverse_lazy('users:profile')
    login_url = '/login/'

    def get_object(self, queryset=None):
        return self.request.user


class Message:
    LOGIN_INVALID = "Invalid Username and Password"
    LOGIN_MISSING = "Missing Username and Password"
    LOGIN_DISABLED = "Disabled Account"

    SIGNUP_MISSING = "Please fill out all the fields"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile_view.html"
    login_url = '/users/login/'


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
    login_url = '/users/login/'


class LogoutView(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        return reverse('users:login')
