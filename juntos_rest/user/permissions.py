from rest_framework import permissions


class StaffPermission(permissions.BasePermission):
    """
    Global permission check for staff user.
    """

    def has_permission(self, request, view):
        return request.user.is_staff


class NotLoggedIn(permissions.BasePermission):
    """
    Global permission check for not logged in user.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated
