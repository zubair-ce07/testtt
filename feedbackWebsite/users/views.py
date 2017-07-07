from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views.generic import RedirectView, TemplateView, View

from .forms import UserLoginForm, UserProfileForm, UserRegisterForm


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


class UserLoginFormView(View):
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


class UserUpdate(LoginRequiredMixin, View):
    form = UserProfileForm
    template_name = 'users/edit.html'

    def get(self, request):
        form = self.form(initial={'email': request.user.email,
                                  'first_name': request.user.first_name,
                                  'last_name': request.user.last_name,
                                  'mobile_number': request.user.profile.mobile_number,
                                  'current_address': request.user.profile.current_address,
                                  'permanent_address': request.user.profile.permanent_address
                                  })

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        active_user = request.user
        if form.is_valid():
            active_user.email = form.cleaned_data["email"]
            active_user.first_name = form.cleaned_data["first_name"]
            active_user.last_name = form.cleaned_data["last_name"]
            active_user.profile.mobile_number = form.cleaned_data["mobile_number"]
            active_user.profile.current_address = form.cleaned_data["current_address"]
            active_user.profile.permanent_address = form.cleaned_data["permanent_address"]
            password = form.cleaned_data["password"]
            if password:
                active_user.set_password(password)
            active_user.save()
            return redirect('users:profile')
        return redirect('users:view')


class Message:
    LOGIN_INVALID = "Invalid Username and Password"
    LOGIN_MISSING = "Missing Username and Password"
    LOGIN_DISABLED = "Disabled Account"

    SIGNUP_MISSING = "Please fill out all the fields"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile_view.html"


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"


class LogoutView(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        return reverse('users:login')
