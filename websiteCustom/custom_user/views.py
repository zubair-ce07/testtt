from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import RedirectView, TemplateView, View
from django.views.generic.edit import UpdateView

from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm


class UserRegisterFormView (View):
    form_class = UserRegisterForm
    template_name = 'custom_user/register.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('custom_user:profile')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('custom_user:login')
        return render(request, self.template_name, {'form': form})


class UserLoginFormView (View):
    form_class = UserLoginForm
    template_name = 'custom_user/login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('custom_user:profile')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'error': ' '})

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        message = Message.LOGIN_DISABLED
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('custom_user:profile')
            message = Message.LOGIN_INVALID
        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form, 'error': message})


class UserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'custom_user/edit.html'
    success_url = reverse_lazy('custom_user:profile')
    login_url = '/custom_user/login/'

    def get_object(self, queryset=None):
        return self.request.user


class Message:
    LOGIN_INVALID = "Invalid Username and Password"
    LOGIN_MISSING = "Missing Username and Password"
    LOGIN_DISABLED = "Disabled Account"

    SIGNUP_MISSING = "Please fill out all the fields"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "custom_user/profile_view.html"
    login_url = '/custom_user/login/'


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = "custom_user/profile.html"
    login_url = '/custom_user/login/'


class LogoutView(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        return reverse('custom_user:login')
