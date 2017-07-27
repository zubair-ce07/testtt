from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from user.forms import LoginForm, SignUpForm
from user.models import UserProfile


class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'user/index.html'
    redirect_field_name = 'username'


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('wblog_user:login')


class Update(UpdateView):
    model = UserProfile
    template_name = 'user/update.html'


class Logout(LogoutView):
    next_page = '/wblog'

