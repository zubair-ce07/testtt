from django.http import HttpResponseRedirect
from django.urls import reverse


def admin_only(view_func):
    """
    Decorator to test the user is admin or not.
    """
    def wrap(instance, *args, **kwargs):
        if instance.request.role == "Admin":
            return view_func(instance, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('ballot:ballot_list'))

    return wrap
