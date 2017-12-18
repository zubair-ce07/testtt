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


class IsCreateOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated() and request.user.is_admin
        elif view.action == 'create':
            return request.user.is_anonymous
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.user.is_authenticated()
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated() and (obj == request.user or request.user.is_admin)
        elif view.action == 'destroy':
            return request.user.is_authenticated() and request.user.is_admin
        else:
            return False
