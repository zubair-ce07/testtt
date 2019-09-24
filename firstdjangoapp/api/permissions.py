from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class AllowAnyOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
        return request.user.is_superuser
