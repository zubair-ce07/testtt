from django.shortcuts import render


def handler404(request, exception):
    locals().update({'error': '404'})
    return render(request, 'errors/errors.html', locals())
