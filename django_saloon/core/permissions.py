"""permission module"""
from rest_framework import permissions


class IsShop(permissions.BasePermission):
    """
     Global permission to check if user is Shop.
     """

    def has_permission(self, request, view):
        return hasattr(request.user, 'shop')


class IsCustomer(permissions.BasePermission):
    """
    Global permission to check if user is Customer.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'customer')


class IsShopOwnerOrReservedSloTCustomer(permissions.BasePermission):
    """
    Object-level permission to only allow shop owners or reservation
    customer of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'customer'):
            return request.user.customer == obj.customer
        if hasattr(request.user, 'shop'):
            return request.user.shop == obj.time_slot.saloon
        return False
