"""Shop views model."""
from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from customer.forms import UserUpdateForm
from shop.forms import ShopUpdateForm
from shop.models import Saloon, TimeSlot, Reservation
from shop.serializers import ShopSerializer
from shop.serializers import (
    SaloonUpdateSerializer, TimeSlotSerializer,
    TimeSlotSerializerForCustomers,
    ScheduleSerializer, ReservationSerializer,
    AddReviewSerializer, ListReservationSerializer
)
from core.permissions import (
    IsCustomer, IsShop, IsShopOwnerOrReservedSloTCustomer,
    IsReservedSloTCustomerAndReviewNotAdded
)
from core.constants import (
    CUSTOMER, SALOON, SHOP_NAME, TIME,
    START_TIME, END_DATE, START_DATE,
    NUMBER_OF_SLOTS, REASON, SLOT_ID, SLOT_DURATION
)


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Render and Save Profile Form.

    This method renders the user and shop update form and also save it's data
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
        """Check if user is saloon user."""
        return hasattr(self.request.user, SALOON)


class SaloonListView(ListView):
    """List saloons."""

    model = Saloon
    template_name = 'shop/saloons.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'saloons'
    ordering = [SHOP_NAME]
    paginate_by = 5


class MyShopListView(LoginRequiredMixin, UserPassesTestMixin, ListView, View):
    """Lists timeslots of a user saloon."""

    model = TimeSlot
    template_name = 'shop/mysaloon.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'time_slots'
    ordering = [TIME]
    paginate_by = 12

    def get_queryset(self):
        """Filter TimeSlot object for user saloon."""
        return TimeSlot.objects.filter(saloon=self.request.user.saloon).order_by('time')

    def post(self, request):
        """POST method for Profile View.

        This method will save profile data when profile form is submitted if
        form is valid and then create timeslot object in db for given schedule.
        """
        start_time = request.POST.get(START_TIME, None)
        number_of_slots = request.POST.get(NUMBER_OF_SLOTS, None)
        slot_duration = request.POST.get(SLOT_DURATION, None)
        saloon = self.request.user.saloon
        slots = []
        if int(start_time)+((int(number_of_slots) * int(slot_duration))/60) > 24:
            messages.warning(
                request, f'Time slots are exceding one day after the start time!')
            return redirect('my_shop')

        start_date = datetime.strptime(
            request.POST.get(START_DATE, None), '%Y-%m-%d')
        end_date = datetime.strptime(
            request.POST.get(END_DATE, None), '%Y-%m-%d')

        if start_date > end_date:
            messages.warning(
                request, f'start date is greater than end date!')
            return redirect('my_shop')

        day_count = (end_date - start_date).days + 1
        for single_date in (start_date + timedelta(n) for n in range(day_count)):
            for slot in range(int(number_of_slots)):
                slots.append(
                    TimeSlot(
                        saloon=saloon, time=single_date + timedelta(hours=int(start_time),
                                                                    minutes=slot*int(slot_duration))))
        TimeSlot.objects.bulk_create(slots)
        messages.success(
            request, f'Time slots added!')
        return redirect('my_shop')

    def test_func(self):
        """Check if user is saloon user."""
        return hasattr(self.request.user, SALOON)


class SaloonSlotListView(LoginRequiredMixin, UserPassesTestMixin, ListView, View):
    """List a saloon time slots."""

    model = TimeSlot
    template_name = 'shop/shop_slot_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'time_slots'
    paginate_by = 12

    def get_queryset(self):
        """Filter timeslots for the given saloon."""
        saloon = get_object_or_404(
            Saloon, shop_name=self.kwargs.get(SHOP_NAME))
        return TimeSlot.objects.filter(saloon=saloon).order_by(TIME)

    @staticmethod
    def post(request, shop_name):
        """POST method for SaloonSlotListView View.

        This method will save create a reservation object and save it to db.
        """
        slot_id = request.POST.get(SLOT_ID, None)
        slot = TimeSlot.objects.get(id=slot_id)

        Reservation(customer=request.user.customer, time_slot=slot).save()
        messages.success(
            request, f'Time slots reserved!')
        return redirect('shop_list')

    def test_func(self):
        """Checks if user is customer user."""
        return hasattr(self.request.user, CUSTOMER)


class ReservationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Lists a shop reserved slots."""

    model = Reservation
    template_name = 'shop/myreservations.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'reservations'
    paginate_by = 8

    def get_queryset(self):
        """Filter a shop reserved slots."""
        return Reservation.objects.filter(time_slot__saloon=self.request.user.saloon)

    @staticmethod
    def post(request):
        """POST method for shop ReservationsListView.

        This method will delete reservation.
        """
        reservation_id = request.POST.get("reservation_id", " ")
        _ = request.POST.get(REASON, None)
        Reservation.objects.get(id=reservation_id).delete()
        messages.success(
            request, f'Reservation Cancelled!')
        return redirect('shop_reservations')

    def test_func(self):
        """Check if user is customer user."""
        return hasattr(self.request.user, SALOON)


class ShopListApiView(generics.ListAPIView):
    """Api shop list view."""

    queryset = Saloon.objects.all()
    serializer_class = ShopSerializer


class ShopUpdateApiView(APIView):
    """Customer update view for api.

     post method data structure
    {
        "user":{
        "username":"username",
        "email":"abc@gmail.com",
        "firstname":"abc",
        "last_name":"xyz"
        },
        "phone_no":0051315,
        "address":"h_no 123, xyz city",
        "shop_name":"xyz saloon"
    }
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated, IsShop)

    @staticmethod
    def post(request):
        """Post method for customer update."""
        instance = request.user
        saloon_update_serializer = SaloonUpdateSerializer(
            instance=instance.saloon, data=request.data
        )
        if saloon_update_serializer.is_valid(raise_exception=True):
            saloon_update_serializer.save()
        return Response(data={"shop updated successfully"}, status=status.HTTP_200_OK)


class ListAddTimeSlotsApiView(generics.ListCreateAPIView):
    """List time slots of a saloon api view."""

    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()
    permission_classes = (IsAuthenticated, IsShop)

    def get_queryset(self):
        """Override queryset."""
        return self.queryset.filter(saloon=self.request.user.saloon.id)

    def post(self, request, *args, **kwargs):
        """List Add TimeSlots post method.

        post request data format
        {
            "start_date":"2019-08-26",
            "end_date":"2019-08-27",
            "start_time":"08",
            "no_hours":"08"
        }
        """
        # schedule data from post request
        schedule_serializer = ScheduleSerializer(data=request.data)
        slots = []
        if schedule_serializer.is_valid(raise_exception=True):
            start_date = schedule_serializer.validated_data[START_DATE]
            end_date = schedule_serializer.validated_data[END_DATE]
            start_time = schedule_serializer.validated_data[START_TIME]
            number_of_slots = schedule_serializer.validated_data[NUMBER_OF_SLOTS]
            slot_duration = schedule_serializer.validated_data[SLOT_DURATION]

            if int(start_time)+((int(number_of_slots) * int(slot_duration))/60) > 24:
                return Response(
                    data={"Time slots are exceding one day after the start time!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if start_date > end_date:
                return Response(
                    data={"start date is greater than end date!"},
                    status=status.HTTP_400_BAD_REQUEST)

            day_count = (end_date - start_date).days + 1
            for single_date in (start_date + timedelta(n) for n in range(day_count)):
                for slot in range(int(number_of_slots)):
                    slot_time = datetime.min + timedelta(hours=int(start_time),
                                                         minutes=slot*int(slot_duration))
                    slots.append(
                        TimeSlot(saloon=self.request.user.saloon,
                                 time=datetime.combine(
                                     single_date, slot_time.time())
                                 )
                    )
            TimeSlot.objects.bulk_create(slots)
            return Response(data={"slots added  successfully"}, status=status.HTTP_200_OK)
        return Response(data={"Data not valid!"}, status=status.HTTP_400_BAD_REQUEST)


class ListSaloonSlotsApiView(generics.ListAPIView):
    """List saloon slots by name."""

    serializer_class = TimeSlotSerializerForCustomers
    queryset = TimeSlot.objects.all()
    permission_classes = (IsAuthenticated, IsCustomer)

    def get_queryset(self):
        """Override queryset."""
        return TimeSlot.objects.filter(saloon__shop_name=self.kwargs.get(SHOP_NAME))


class DeleteReservationApiView(generics.DestroyAPIView):
    """Delete reservation only by customer or shop."""

    permission_classes = (IsAuthenticated, IsShopOwnerOrReservedSloTCustomer)
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class ShopReservationsApiView(generics.ListAPIView):
    """List a saloon reservations."""

    serializer_class = ListReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthenticated, IsShop)

    def get_queryset(self):
        """Override querset."""
        return Reservation.objects.filter(
            time_slot__saloon=self.request.user.saloon)


class ReserveTimeSlotApiView(generics.CreateAPIView):
    """Reserve a slot by customer.

    post request data format
    {
    "time_slot": 748
    }
    """

    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthenticated, IsCustomer)

    def post(self, request, *args, **kwargs):
        """Post method for reserve time slot."""
        request.data['customer'] = request.user.customer.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data={"slot reserved successfully"}, status=status.HTTP_200_OK)


class AddReviewApiView(generics.CreateAPIView):
    """Add review api view."""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated, IsCustomer,
                          IsReservedSloTCustomerAndReviewNotAdded)

    serializer_class = AddReviewSerializer

    def post(self, request, *args, **kwargs):
        """Post method for add review."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data={"review added sucessfully"}, status=status.HTTP_200_OK)
