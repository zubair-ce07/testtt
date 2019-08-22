from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as auth_logout

from .forms import UserRegisterForm, UserUpdateForm, CustomerUpdateForm
from .models import Customer


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
            user_form.instance.is_customer = True
            user = user_form.save()
            Customer.objects.create(user=user)
            messages.success(request, f'Your account has been Created!')
            return redirect('login')
        return render(request, 'customer/register.html', {'user_form': user_form})

    @staticmethod
    def get(request):
        """Register GET method.

        this method will save the user data when form is submitted
        """
        user_form = UserRegisterForm()
        return render(request, 'customer/register.html', {'user_form': user_form})


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
        customer_update_form = CustomerUpdateForm(
            request.POST, instance=request.user.customer)
        if user_update_form.is_valid() and customer_update_form.is_valid():
            user_update_form.save()
            customer_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('customer_profile')
        return render(request, 'customer/profile.html', {'user_form': user_update_form, 'customer_form': customer_update_form})

    @method_decorator(login_required)
    @staticmethod
    def get(request):
        """GET method for Profile Form.
        This method will render profile form.
        """
        user_update_form = UserUpdateForm(instance=request.user)
        customer_update_form = CustomerUpdateForm(
            instance=request.user.customer)

        return render(request, 'customer/profile.html', {'user_form': user_update_form, 'customer_form': customer_update_form})


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
