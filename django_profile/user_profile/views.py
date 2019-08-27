"""User Profile Views module.

This module contains differnet views for user profile app.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.generic.edit import FormView

from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm


class Register(View):
    """Render and save user to profile

    This method renders the user registration form and also save it's data
    when form is submitted
    """
    @staticmethod
    def post(request):
        """Register POST method.

        This method will render the registration from
        """
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your account has been Created!')
            return redirect('login')
        return render(request, 'user_profile/register.html', {'form': user_form})

    @staticmethod
    def get(request):
        """Register GET method.

        this method will save the user data when form is submitted
        """
        user_form = UserRegisterForm()
        return render(request, 'user_profile/register.html', {'form': user_form})


class Profile(View):
    """Render and Save Profile Form.

    This method renders the profile form and also save it's data
    when form is submitted
    """

    @method_decorator(login_required)
    @staticmethod
    def post(request):
        """POST method for Profile View.
        This method will save profile data when profile form is submitted.
        """
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        return render(request, 'user_profile/profile.html', {'form': user_update_form})

    @method_decorator(login_required)
    @staticmethod
    def get(request):
        """GET method for Profile Form.
        This method will render profile form.
        """
        user_update_form = UserUpdateForm(instance=request.user)
        context = {
            'form': user_update_form
        }

        return render(request, 'user_profile/profile.html', context)


class LogoutView(View):
    """Log out User.

    This logout user View
    """

    @staticmethod
    def get(request):
        """Log out User.

        This method logout user and redirect it to login page
        """
        auth_logout(request)
        return redirect('login')


class LoginView(FormView):
    """Login user Form
    Display the login form and handle the login action.
    """
    template_name = 'user_profile/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return redirect('profile')
