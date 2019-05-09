from pprint import pprint

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        pprint(type(obj))
        pprint(obj)
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.user_id
