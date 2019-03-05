from rest_framework import permissions


class IsIssueOwner(permissions.BasePermission):
    message = "You are not allowed to View this Issue"

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user


class IsCommentOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = "You are not allowed to edit this comment"

    def has_object_permission(self, request, view, obj):
        return obj.comment_by == request.user


class IsCustomerOrManager(permissions.BasePermission):
    message = "You are not allowed to View/Create Issue"

    def has_permission(self, request, view):
        return (request.user.groups.first().name == 'Customer' or
                request.user.groups.first().name == 'Manager')
