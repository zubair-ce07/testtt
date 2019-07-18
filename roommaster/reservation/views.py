from django.shortcuts import render
from django.http import HttpResponse
from .models import Room, Customer, Employee, Reservation


def home(request):
    return render(request, 'reservation/home.html')


def rooms(request):
    rooms = {
        'rooms': Room.objects.all(),
        'length': len(Room.objects.all())
    }
    return render(request, 'reservation/rooms.html', rooms)


def customers(request):
    customers = {
        'customers': Customer.objects.all(),
        'length': len(Customer.objects.all())
    }
    return render(request, 'reservation/customers.html', customers)


def employees(request):
    employees = {
        'employees': Employee.objects.all(),
        'length': len(Employee.objects.all())
    }
    return render(request, 'reservation/employees.html', employees)


def reservations(request):
    reservations = {
        'reservations': Reservation.objects.all(),
        'length': len(Reservation.objects.all())
    }
    return render(request, "reservation/reservations.html", reservations)
