from django.shortcuts import render
from django.http import HttpResponse
from reservation.models import Room, Customer, Employee, Reservation


def home(request):
    return render(request, 'reservation/home.html')


def rooms(request):
    return render(request, 'reservation/rooms.html', {'rooms': Room.objects.all()})


def customers(request):
    return render(request, 'reservation/customers.html',  {'customers': Customer.objects.all()})


def employees(request):
    return render(request, 'reservation/employees.html', {'employees': Employee.objects.all()})


def reservations(request):
    return render(request, "reservation/reservations.html", {'reservations': Reservation.objects.all()})
