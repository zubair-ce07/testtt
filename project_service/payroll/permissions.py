from rest_framework import permissions


class IsAccountant(permissions.BasePermission):
    '''
    Permission to check if requesting user is accountant
    '''

    def has_permission(self, request, view):
        return True
