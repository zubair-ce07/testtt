from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views

from .models import User
from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm
# Create your views here.


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been Created!')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'user_profile/register.html', {'form': form})


class Register(View):
    def post(self, request):
        form = UserRegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been Created!')
            return redirect('login')
        return render(request, 'user_profile/register.html', {'form': form})

    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user_profile/register.html', {'form': form})


"""User Profile Views module.

This module contains differnet views for user profile app.
"""


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
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    @method_decorator(login_required)
    def get(self, request):
        """GET method for Profile Form.
        This method will render profile form.
        """
        form = UserUpdateForm(instance=request.user)
        context = {
            'form': form
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
