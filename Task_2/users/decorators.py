from django.http import HttpResponseRedirect
from django.urls import reverse


def login_required(function):
    def wrap(request, *args, **kwargs):
        if 'userid' not in request.session.keys():
            return HttpResponseRedirect(redirect_to=reverse('users:login') + "?next=" + request.path)
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
