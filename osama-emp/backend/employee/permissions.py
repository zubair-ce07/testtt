from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    Custom permission to open only profile of self
    """

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class IsDirect(permissions.BasePermission):
    """
    Custom permission to check if logged in user has directs
    """

    def has_object_permission(self, request, view, obj):
        print(obj)
        print(request)
        return (obj == request)
