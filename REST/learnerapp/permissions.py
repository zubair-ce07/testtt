from rest_framework import permissions

from learnerapp import constants, models


class UserOnlyUpdatePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to update it.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if request.user.user_type == constants.STUDENT:
                user = models.Student.objects.get(user__pk=request.user.id)
                if request.method in ('PUT',) and user.id == int(view.kwargs['pk']):
                    return True
            return [False, True][request.user.user_type == constants.TEACHER or
                                 request.method in permissions.SAFE_METHODS]
        return False


class InstructorAddPermission(permissions.BasePermission):
    """
    Custom permission to only allow Instructors to add instructors
    """
    message = 'Authorization required'

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return obj.user == request.user
        return True

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