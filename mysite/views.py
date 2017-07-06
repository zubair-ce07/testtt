from django.http import HttpResponse, Http404
import datetime
from django.template.loader import get_template
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world")


def homepage(request):
    return HttpResponse("Homepage")


def current_date_time(request):
    now = datetime.datetime.now()
    #t = get_template('current_datetime.html')
   # html = t.render({'current_date': now})
    return render(request, 'current_datetime.html', {'current_date': now, 'current_section': 'blul'})


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'hours_ahead.html', {'hours_offset': offset, 'next_time': dt})


def html_meta(request):
    values = request.META
    html = []
    for val in values:
        html.append((val,values[val]))
    return render(request, 'html_meta.html', {'values': html, })
