import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render


def homepage(request):
    return render(request, 'base.html')


def current_date_time(request):
    time_now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': time_now})


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404('Enter a number in the range of 0-99 instead of a character')
    time_ahead = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'hours_ahead.html', {'hours_offset': offset, 'next_time': time_ahead})


def html_meta(request):
    html = [(val, request.META[val]) for val in request.META]
    return render(request, 'html_meta.html', {'values': html})
