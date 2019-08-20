"""User Profile Views module.

This module contains differnet views for user profile app.
"""
from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.generic.edit import FormView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.contrib.sites.shortcuts import get_current_site

from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm


class Register(View):
    """Render and save user to profile

    This method renders the user registration form and also save it's data
    when form is submitted
    """

    def post(self, request):
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your account has been Created!')
            return redirect('login')
        return render(request, 'user_profile/register.html', {'form': user_form})

    def get(self, request):
        user_form = UserRegisterForm()
        return render(request, 'user_profile/register.html', {'form': user_form})


class Profile(View):
    """Render and Save Profile Form.

    This method renders the profile form and also save it's data
    when form is submitted
    """

    @method_decorator(login_required)
    def post(self, request):
        """POST method for Profile Form.
        This method will save profile data when profile form is submitted.
        """
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        return render(request, 'user_profile/profile.html', {'form': user_update_form})

    @method_decorator(login_required)
    def get(self, request):
        """GET method for Profile Form.
        This method will render profile form.
        """
        user_update_form = UserUpdateForm(instance=request.user)
        context = {
            'form': user_update_form
        }

        return render(request, 'user_profile/profile.html', context)


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('login')


class LoginView(auth_views.SuccessURLAllowedHostsMixin, FormView):
    """Login user Form
    Display the login form and handle the login action.
    """
    template_name = 'user_profile/login.html'
    form_class = UserLoginForm
    authentication_form = None
    redirect_field_name = 'next'
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('profile')

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context
