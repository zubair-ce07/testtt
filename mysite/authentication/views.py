from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.utils.http import is_safe_url
from .forms import UserCreationForm, LoginForm


class SignupView(View):
    template_name = 'authentication/signup.html'
    form_class = UserCreationForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('super_store:brands'))

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('super_store:brands'))

        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect(
                reverse('super_store:brands'))
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    template_name = 'authentication/login.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('authentication:login'))


class LoginView(View):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('super_store:brands'))

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('super_store:brands'))

        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(self.request, user)
                    redirect_to = request.GET.get('next', '')
                    if redirect_to != '':
                        if is_safe_url(url=redirect_to, host=request.get_host()):
                            return redirect(redirect_to)
                        else:
                            return render(self.request, redirect_to,
                                          {'error': message, 'form': form})
                    else:
                        return redirect(reverse('super_store:brands'))
                else:
                    message = Message.LOGIN_DISABLED
            else:
                message = Message.LOGIN_INVALID

        return render(self.request, self.template_name,
                      {'error': message, 'form': form})


class Message:
    LOGIN_INVALID = "Invalid Username and Password"
    LOGIN_MISSING = "Missing Username and Password"
    LOGIN_DISABLED = "Disabled Account"
    SIGNUP_MISSING = "Please fill out all the fields"
