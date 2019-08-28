"""core view module"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

from core.forms import UserRegisterForm
from shop.models import Saloon
from customer.models import Customer


class LogoutView(View):
    """Log out User view."""

    @staticmethod
    def get(request):
        """Log out User and clear it's session and cookies.
        """
        auth_logout(request)
        return redirect('login')


class UserRegisterView(View):
    """Render and save shop user

    This method renders the user registration form and also save it's data
    when form is submitted
    """
    @staticmethod
    def post(request):
        """UserRegisterView POST method."""
        user_form = UserRegisterForm(request.POST)
        user_type = request.POST.get("user_type", None)
        if user_form.is_valid():
            user = user_form.save()
            if user_type == 'customer':
                Customer.objects.create(user=user)
            else:
                Saloon.objects.create(user=user)

            messages.success(request, f'Your account has been Created!')
            return redirect('login')
        return render(request, 'core/register.html', {'user_form': user_form})

    @staticmethod
    def get(request):
        """UserRegisterView GET method."""
        user_form = UserRegisterForm()
        return render(request, 'core/register.html', {'user_form': user_form})
