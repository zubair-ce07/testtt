from rest_framework import permissions


class UserOnlyUpdatePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to update it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return obj.user == request.user
        return True