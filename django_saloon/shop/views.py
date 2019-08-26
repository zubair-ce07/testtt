from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime, timedelta
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.conf import settings


from customer.forms import UserRegisterForm, UserUpdateForm
from .forms import ShopUpdateForm
from .models import Saloon, TimeSlot, Reservation


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
        return render(request, 'customer/register.html', {'user_form': user_form, 'form_title': 'Sign Up to add your saloon'})

    @staticmethod
    def get(request):
        """Register GET method.

        this method will save the user data when form is submitted
        """
        user_form = UserRegisterForm()
        return render(request, 'customer/register.html', {'user_form': user_form, 'form_title': 'Sign Up to add your saloon'})


class Profile(LoginRequiredMixin, UserPassesTestMixin, View):
    """Render and Save Profile Form.

    This method renders the profile form and also save it's data
    when form is submitted
    """

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

    @staticmethod
    def get(request):
        """GET method for Profile Form.
        This method will render profile form.
        """
        user_update_form = UserUpdateForm(instance=request.user)
        shop_update_form = ShopUpdateForm(
            instance=request.user.saloon)

        return render(request, 'shop/profile.html', {'user_form': user_update_form, 'shop_form': shop_update_form})

    def test_func(self):
        return hasattr(self.request.user, 'saloon')


class SaloonListView(ListView):
    model = Saloon
    template_name = 'shop/saloons.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'saloons'
    ordering = ['shop_name']
    paginate_by = 5


class MyShopListView(LoginRequiredMixin, UserPassesTestMixin, ListView, View):
    model = TimeSlot
    template_name = 'shop/mysaloon.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'time_slots'
    ordering = ['time']
    paginate_by = 12

    def get_queryset(self):
        return TimeSlot.objects.filter(saloon=self.request.user.saloon).order_by('time')

    def post(self, request):
        """POST method for Profile View.
        This method will save profile data when profile form is submitted.
        """
        start_time = request.POST.get("start_time", " ")
        # minutes = request.POST.get("minutes", " ")
        no_hours = request.POST.get("no_hours", " ")
        saloon = self.request.user.saloon
        slots = []
        if int(start_time)+int(no_hours) > 24:
            messages.warning(
                request, f'Time slots are exceding one day after the start time!')
            return redirect('my_shop')
        else:
            start_date = datetime.strptime(
                request.POST.get("start_date", " "), '%Y-%m-%d')
            end_date = datetime.strptime(
                request.POST.get("end_date", " "), '%Y-%m-%d')
            day_count = (end_date - start_date).days + 1
            for single_date in (start_date + timedelta(n) for n in range(day_count)):
                for slot in range(int(no_hours)):
                    slots.append(
                        TimeSlot(saloon=saloon, time=single_date + timedelta(hours=int(start_time)+slot)))
            TimeSlot.objects.bulk_create(slots)
            messages.success(
                request, f'Time slots added!')

        return redirect('my_shop')

    def test_func(self):
        return hasattr(self.request.user, 'saloon')


class SaloonSlotListView(LoginRequiredMixin, UserPassesTestMixin, ListView, View):
    model = TimeSlot
    template_name = 'shop/shop_slot_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'time_slots'
    paginate_by = 12

    def get_queryset(self):
        saloon = get_object_or_404(
            Saloon, shop_name=self.kwargs.get('shop_name'))
        return TimeSlot.objects.filter(saloon=saloon).order_by('time')

    def post(self, request, shop_name):
        """POST method for Profile View.
        This method will save profile data when profile form is submitted.
        """
        slot_id = request.POST.get("slot_id", " ")
        slot = TimeSlot.objects.get(id=slot_id)

        Reservation(customer=request.user.customer, time_slot=slot).save()
        messages.success(
            request, f'Time slots reserved!')
        return redirect('shop_list')

    def test_func(self):
        return hasattr(self.request.user, 'customer')


class ReservationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Reservation
    template_name = 'shop/myreservations.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'reservations'
    paginate_by = 8

    def get_queryset(self):
        return Reservation.objects.filter(time_slot__saloon=self.request.user.saloon)

    def post(self, request):
        """POST method for Profile View.
        This method will save profile data when profile form is submitted.
        """
        res_id = request.POST.get("res_id", " ")
        reason = request.POST.get("reason", " ")
        Reservation.objects.get(id=res_id).delete()
        messages.success(
            request, f'Reservation Cancelled!')
        return redirect('shop_reservations')

    def test_func(self):
        return hasattr(self.request.user, 'saloon')
