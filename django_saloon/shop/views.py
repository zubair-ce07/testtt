from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

from customer.forms import UserRegisterForm, UserUpdateForm
from .forms import ShopUpdateForm
from .models import Saloon


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
            Saloon.objects.create(user=user)
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
        shop_update_form = ShopUpdateForm(
            request.POST, instance=request.user.saloon)
        if user_update_form.is_valid() and shop_update_form.is_valid():
            user_update_form.save()
            shop_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('shop_profile')
        return render(request, 'shop/profile.html', {'user_form': user_update_form, 'shop_form': shop_update_form})

    @method_decorator(login_required)
    @staticmethod
    def get(request):
        """GET method for Profile Form.
        This method will render profile form.
        """
        user_update_form = UserUpdateForm(instance=request.user)
        shop_update_form = ShopUpdateForm(
            instance=request.user.saloon)

        return render(request, 'shop/profile.html', {'user_form': user_update_form, 'shop_form': shop_update_form})
