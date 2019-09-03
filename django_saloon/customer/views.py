"""Customer app view module.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status


from customer.forms import UserUpdateForm, CustomerUpdateForm
from customer.serializers import CustomerUpdateSerializer
from shop.serializers import ReservationSerializer
from shop.models import Reservation
from core.permissions import IsCustomer
from core.constants import CUSTOMER, RESERVATION_ID, REASON


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
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
        return render(request, 'customer/profile.html', {'user_form': user_update_form,
                                                         'customer_form': customer_update_form})

    @staticmethod
    def get(request):
        """GET method for Profile Form.
        This method will render profile form.
        """
        user_update_form = UserUpdateForm(instance=request.user)
        customer_update_form = CustomerUpdateForm(
            instance=request.user.customer)

        return render(request, 'customer/profile.html', {'user_form': user_update_form,
                                                         'customer_form': customer_update_form})

    def test_func(self):
        return hasattr(self.request.user, CUSTOMER)


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

    @staticmethod
    def post(request):
        """POST method for Reservation View.
        This method will delete a reservation shich id is send through post request from template.
        """
        reservation_id = request.POST.get(RESERVATION_ID, None)
        _ = request.POST.get(REASON, None)
        Reservation.objects.get(id=reservation_id).delete()
        messages.success(
            request, f'Reservation Cancelled!')
        return redirect('customer_reservations')

    def test_func(self):
        """only customer can access this view"""
        return hasattr(self.request.user, CUSTOMER)


class CustomerUpdateApiView(APIView):
    """customer update view for api.
    post method data structure
    {
        "user":{
        "username":"username",
        "email":"abc@gmail.com",
        "firstname":"abc",
        "last_name":"xyz"
        },
        "phone_no":0051315
    }
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated, IsCustomer)

    @staticmethod
    def post(request):
        """post method for customer update"""
        instance = request.user
        customer_update_serializer = CustomerUpdateSerializer(
            instance=instance.customer, data=request.data
        )
        if customer_update_serializer.is_valid(raise_exception=True):
            customer_update_serializer.save()
        return Response(data={"customer updated successfully"}, status=status.HTTP_200_OK)


class MyReservationsApiView(generics.ListAPIView):
    """customer reservation list api view"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated, IsCustomer)

    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get_queryset(self):
        """queryset override"""
        return Reservation.objects.filter(
            customer=self.request.user.customer)
