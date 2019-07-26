from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from reservation.models import Room, Customer, Employee, Reservation
from django.views.generic import TemplateView
from django.db.models import Q, Count, Sum
from django.contrib.auth.forms import UserCreationForm
from reservation.form import AvailabilityForm, ReservationForm, RegistrationForm
from django.views.decorators.cache import cache_control
from django.contrib import messages
import datetime


class HomeView(TemplateView):
    template_name = 'reservation/home.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)


class RoomsView(TemplateView):
    template_name = 'reservation/rooms.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {'title': 'Rooms', 'rooms': Room.objects.all()})


class CustomersView(TemplateView):
    template_name = 'reservation/customers.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {'title': 'Customers', 'customers': Customer.objects.all()})


class ReservationsView(TemplateView):
    template_name = 'reservation/reservations.html'    

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {'title': 'Reservations', 'reservations': Reservation.objects.all()})


class EmployeesView(TemplateView):
    template_name = 'reservation/employees.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {'title': 'Employees', 'employees': Employee.objects.all()})


class AvailabilityView(TemplateView):
    template_name = 'reservation/availability.html'

    @method_decorator(login_required)
    def get(self, request):
        form = AvailabilityForm()
        return render(request, self.template_name, {'title': 'Availability', 'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data['checkin']
            checkout = form.cleaned_data['checkout']
            context = {
                'form': form,
                'rooms': Room.objects.exclude((Q(reservation__checkin__lte=checkin) &
                                               Q(reservation__checkout__gte=checkin)) | (
                                               Q(reservation__checkin__lte=checkout) &
                                               Q(reservation__checkout__gte=checkout))),
                'checkin': checkin,
                'checkout': checkout
            }
            return render(request, self.template_name, context)


class ReportView(TemplateView):
    template_name = 'reservation/report.html'

    @method_decorator(login_required)
    def get(self, request):
        today = datetime.date.today().strftime('%Y-%m-%d')
        month = datetime.date.today().strftime('%m')
        context = {
            'date': datetime.date.today().strftime('%B %d, %Y'),
            'daily_reservations': Reservation.objects.filter(checkin=today).count(),
            'monthly_reservations': Reservation.objects.filter(checkin__month = month).count(),
            'available_rooms': Room.objects.exclude(Q(reservation__checkin__lte=today) & Q(reservation__checkout__gte=today)).count(),
            'rooms': Room.objects.exclude(Q(reservation__checkin__lte=today) & Q(reservation__checkout__gte=today)),
            'total_employees': Employee.objects.count(),
            'employees': Employee.objects.values('designation').annotate(dcount=Count('designation')),
            'today_income': Reservation.objects.filter(checkin=today).aggregate(Sum('rent'))["rent__sum"],
            'monthly_income': Reservation.objects.filter(checkin__month=month).aggregate(Sum('rent'))["rent__sum"]
        }
        return render(request, self.template_name, context)


class ReserveRoomView(TemplateView):
    template_name = 'reservation/reserveroom.html'

    @method_decorator(login_required)
    def get(self, request, id, checkin, checkout):
        form = ReservationForm(room=Room.objects.filter(id=id)[0], checkin=checkin, checkout=checkout)
        return render(request, self.template_name, {'form': form})


class AddReservation(TemplateView):
    @method_decorator(login_required)
    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            room = Room.objects.filter(room_no=form.cleaned_data.get('room'))[0]
            rent = form.cleaned_data.get('rent')
            customer = form.cleaned_data.get('customer')
            checkin = form.cleaned_data.get('checkin')
            checkout = form.cleaned_data.get('checkout')
            Reservation(room=room, rent=rent, customer=customer, checkin=checkin, checkout=checkout).save()
            messages.success(request, f'Room #{room} is reserved from {checkin} to {checkout}')
            return redirect('reservation-reservations')

        """room = Room.objects.filter(room_no=request.POST.get('room'))[0]
        rent = request.POST.get('rent')
        customer = Customer.objects.filter(id=request.POST.get('customer'))[0]
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')"""


class RegistrationView(TemplateView):
    template_name = 'reservation/register.html'

    @method_decorator(login_required)
    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('reservation-home')

        return render(request, self.template_name, {'form': form})
