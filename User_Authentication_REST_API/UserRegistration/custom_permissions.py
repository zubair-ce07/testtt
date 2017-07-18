from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    """
    Checks if the requested user is superuser or not
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
