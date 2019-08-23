from rest_framework.permissions import BasePermission, SAFE_METHODS


class isAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser


class isSameUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser
