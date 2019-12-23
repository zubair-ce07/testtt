from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import View, FormView
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _

from .forms import LoginForm, SignUpForm


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, LoginView):
    template_name = 'login.html'
    form_class = LoginForm


class SignUpView(GuestOnlyView, FormView):
    template_name = 'sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        user.save()
        messages.success(request, _('You are successfully signed up!'))
        return redirect('login')
