import datetime
from django.shortcuts import render
from django.http import Http404


def current_datetime(request):
    now = datetime.datetime.now()
    return render(
            request,
            'dateapp/current_datetime.html',
            {'current_date': now})


def hours_ahead(request, offset):

    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    now = datetime.datetime.now()
    dt = now + datetime.timedelta(hours=offset)
    return render(
                request,
                'dateapp/hours_ahead.html',
                {'hour_offset': now, 'next_time': dt})
