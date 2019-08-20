"""User Profile Views module.

This module contains differnet views for user profile app.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views

from .models import User
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


class LoginView(auth_views.LoginView):
    """Login view Class.

    This method will render the login form,it inherits LoginView, and override
    it's from class to our login form so that email field is displayed instead
    of username.
    """

    template_name = 'user_profile/login.html'
    form_class = UserLoginForm
