from rest_framework.permissions import BasePermission


class IsEligible(BasePermission):

    def has_permission(self, request, view):
        return False if request.user.is_authenticated else True