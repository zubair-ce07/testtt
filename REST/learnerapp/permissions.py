from rest_framework import permissions

from learnerapp import constants


class UserOnlyUpdatePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to update it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return obj.user == request.user
        return True

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class InstructorAddPermission(permissions.BasePermission):
    """
    Custom permission to only allow Instructors to add new instructors
    """
    message = 'Authorization required'

    def has_permission(self, request, view):
        if request.user.is_authenticated():
            return [False, True][request.user.user_type == constants.TEACHER]
        return False


class InstructorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow instructors to add courses.
    """
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.user_type == constants.TEACHER if request.user.is_authenticated() \
                else False
        return True