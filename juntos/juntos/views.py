from django.shortcuts import render


def handler404(request, exception):
    """
    Handler for error 404.
    :param request: Request object
    :param exception: Exception
    :return: render error page.
    """
    locals().update({'error': '404'})
    return render(request, 'errors/errors.html', locals())
