"""Customer app view module.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from .forms import UserRegisterForm, UserUpdateForm, CustomerUpdateForm
from .models import Customer
from shop.models import Reservation


class Register(View):
    """Render and save customer user.

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
        return render(request, 'customer/register.html', {'user_form': user_form, 'form_title': 'Sign Up Today'})

    @staticmethod
    def get(request):
        """Register GET method.

        this method will save the user data when form is submitted
        """
        user_form = UserRegisterForm()
        return render(request, 'customer/register.html', {'user_form': user_form, 'form_title': 'Sign Up Today'})


class Profile(LoginRequiredMixin, UserPassesTestMixin, View):
    """Render and Save Profile Form.

    This method renders the user and customer update form and also save it's data
    when form is submitted
    """

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

    @staticmethod
    def get(request):
        """GET method for Profile Form.
        This method will render profile form.
        """
        user_update_form = UserUpdateForm(instance=request.user)
        customer_update_form = CustomerUpdateForm(
            instance=request.user.customer)

        return render(request, 'customer/profile.html', {'user_form': user_update_form, 'customer_form': customer_update_form})

    def test_func(self):
        return hasattr(self.request.user, 'customer')


class LogoutView(View):
    """Log out User view.
    """

    @staticmethod
    def get(request):
        """Log out User and clear it's session and cookies.
        """
        auth_logout(request)
        return redirect('login')


class ReservationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """customer reservation list view.

    this method list all the customer reservations.
    """
    model = Reservation
    template_name = 'customer/myreservations.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'reservations'
    paginate_by = 8

    def get_queryset(self):
        """customer list querry set filtering reservation for that customer only"""
        return Reservation.objects.filter(customer=self.request.user.customer)

    def post(self, request):
        """POST method for Reservation View.
        This method will delete a reservation shich id is send through post request from template.
        """
        res_id = request.POST.get("res_id", " ")
        reason = request.POST.get("reason", " ")
        Reservation.objects.get(id=res_id).delete()
        messages.success(
            request, f'Reservation Cancelled!')
        return redirect('customer_reservations')

    def test_func(self):
        """only customer can access this view"""
        return hasattr(self.request.user, 'customer')
