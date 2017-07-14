from django.http import HttpResponseRedirect
from django.urls import reverse


def user_login_required(f):
    def wrap(request, *args, **kwargs):
        if 'userid' not in request.session.keys():
            return HttpResponseRedirect(redirect_to=reverse('login') + "?next=" + request.path)
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
