from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


def home(request):
    return render(request, 'reservation/home.html')


def rooms(request):
    rooms = {
        'rooms': Room.objects.all()
    }
    return render(request, 'reservation/rooms.html', rooms)
