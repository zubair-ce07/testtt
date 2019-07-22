from django.shortcuts import render
from django.http import HttpResponse
from reservation.models import Room, Customer, Employee, Reservation
from django.views.generic import TemplateView, ListView
from django.db.models import Q

class HomeView(TemplateView):
    template_name = "reservation/home.html"


class RoomsView(ListView):
    model = Room
    template_name = "reservation/rooms.html"
    context_object_name = 'rooms'
    queryset = Room.objects.all()


class CustomersView(ListView):
    model = Customer
    template_name = "reservation/customers.html"
    context_object_name = 'customers'
    queryset = Customer.objects.all()


class ReservationsView(ListView):
    model = Reservation
    template_name = "reservation/reservations.html"
    context_object_name = 'reservations'
    queryset = Reservation.objects.all()


class EmployeesView(ListView):
    model = Employee
    template_name = "reservation/employees.html"
    context_object_name = 'employees'
    queryset = Employee.objects.all()


class Availability(ListView):
    model = Room
    template_name = "reservation/availability.html"
    context_object_name = 'rooms'
    queryset = Room.objects.exclude(Q(reservation__checkin__range=('2019-07-01', '2019-07-03')) | Q(reservation__checkout__range=('2019-07-01', '2019-07-03')))
