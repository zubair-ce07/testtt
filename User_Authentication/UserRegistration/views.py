from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View, RedirectView, FormView
from .forms import LoginForm, CustomUserSignupForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import CustomUser


# Create your views here.
class ProfileView(FormView):
    template_name = "UserRegistration/profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    form = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return render(request, self.template_name)
        else:
            error_not_login = True
            return render(request, "UserRegistration/login.html",
                          {'error_not_login': error_not_login, 'form': self.form})


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
            if CustomUser.objects.filter(username=username).exists():
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
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('users:profile')
        error = True
        return render(request, self.template_name, {'form': form, 'error_fields': error})


class LogoutView(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        return reverse('users:login')
