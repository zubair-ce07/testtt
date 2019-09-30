"""Permission module."""
from rest_framework import permissions

from core.constants import CUSTOMER, SALOON
from shop.models import Reservation


class IsShop(permissions.BasePermission):
    """Global permission to check if user is Shop."""

    def has_permission(self, request, view):
        """Check if user is shop user."""
        return hasattr(request.user, SALOON)


class IsCustomer(permissions.BasePermission):
    """Global permission to check if user is Customer."""

    def has_permission(self, request, view):
        """Check if user is customer user."""
        return hasattr(request.user, CUSTOMER)


class IsShopOwnerOrReservedSloTCustomer(permissions.BasePermission):
    """It allow shop owners or reservation customer of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """Check if user has object writable permission or not."""
        if hasattr(request.user, CUSTOMER):
            return request.user.customer == obj.customer
        if hasattr(request.user, SALOON):
            return request.user.saloon == obj.time_slot.saloon
        return False


class IsReservedSloTCustomerAndReviewNotAdded(permissions.BasePermission):
    """Check if a user is reserved slot customer and review has not been added already."""

    message = 'Adding Review not allowed.'

    def has_permission(self, request, view):
        """Check if user is slot reserved customer and review is not already present."""
        try:
            reservation = Reservation.objects.get(
                id=request.data["reservation"])
        except Reservation.DoesNotExist:
            self.message = 'reservation id not valid'
            return False
        except KeyError:
            self.message = 'reservation id not provided'
            return False
        return reservation.customer == request.user.customer and not hasattr(reservation, 'review')
