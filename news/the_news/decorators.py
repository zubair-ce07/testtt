__author__ = 'luqman'


from django.http import HttpResponseForbidden
from functools import wraps
from django.utils.decorators import available_attrs


def ip_check(function=None, ip_list=[], *args, **kwargs):
    def decorator(view_function, *args, **kwargs):
        @wraps(view_function, assigned=available_attrs(view_function))
        def wrapped_view(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR', None)
            if ip and ip in ip_list:
                if function:
                    return function(request,*args, **kwargs)
                else:
                    return view_function(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        return wrapped_view
    if function:
        return decorator(function, *args, **kwargs)
    else:
        return decorator