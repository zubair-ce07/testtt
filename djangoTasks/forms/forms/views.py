from django.shortcuts import render
from django.template import RequestContext


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def handler400(request):
    return render(request, '400.html', status=400)
