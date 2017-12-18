"""This module contains custom view decorators"""
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse


def is_super_user(function):
    """
    Restricts all users for 'function' except superusers
    :param function: function on which decorator is called
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper


def is_unauthenticated_user(function):
    """
    Restricts all loggedIn users for 'function'
    :param function: function on which decorator is called
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('new_product'))
        return function(request, *args, **kwargs)
    return wrapper
