from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Grants or denies permission for the object to user
    for reading or updating the object
    """
    def has_object_permission(self, request, view, obj):
        """
        Allows reading permissions to all but writing only
        to the owner of the object.

        Arguments:
            request (Request): request object for which permission is required
            view (View): view to which user is accessing
            obj (object): object for which owner is to be determined.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
