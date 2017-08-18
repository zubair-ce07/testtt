from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions ar   `e allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS request.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write pemissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
