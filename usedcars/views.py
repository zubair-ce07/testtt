from .models import UsedCars
from django.views import generic
from django.http import Http404
from django.shortcuts import render


def index_view(request):
    return render(request, 'usedcars/index.html')


def table_page(request):
    try:
        objs = UsedCars.objects.all()
    except UsedCars.DoesNotExist:
        raise Http404("Table Page does not EXIST!")
    return render(request, 'usedcars/tables.html', {'wheels': objs})


def detail_test(request, company_name):
    try:
        objs = UsedCars.objects.all()
    except UsedCars.DoesNotExist:
        raise Http404("Show Car Page does not exist")
    return render(request, 'usedcars/showCars.html', {'usedCars': objs, 'company_name': company_name})


def single_car(request, car_id):
    try:
        obj = UsedCars.objects.get(id=car_id)
    except UsedCars.DoesNotExist:
        raise Http404("Single Car Page does not exist")
    return render(request, 'usedcars/singleCar.html', {'usedCar': obj})
