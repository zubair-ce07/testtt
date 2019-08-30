"""permission module"""
from rest_framework import permissions
from core.constants import CUSTOMER, SALOON


class IsShop(permissions.BasePermission):
    """
     Global permission to check if user is Shop.
     """

    def has_permission(self, request, view):
        return hasattr(request.user, SALOON)


class IsCustomer(permissions.BasePermission):
    """
    Global permission to check if user is Customer.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, CUSTOMER)


class IsShopOwnerOrReservedSloTCustomer(permissions.BasePermission):
    """
    Object-level permission to only allow shop owners or reservation
    customer of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, CUSTOMER):
            return request.user.customer == obj.customer
        if hasattr(request.user, SALOON):
            return request.user.shop == obj.time_slot.saloon
        return False
