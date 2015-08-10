from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect, redirect
from django.utils.decorators import wraps, available_attrs


def is_logged_in(function=None):

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return redirect(reverse('account'))
            else:
                return view_func(request, *args, **kwargs)
        return wrapped_view

    if function:
        return decorator(function)
    return decorator

