from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'You must be the owner of this view'

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 'S'


class IsTutor(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 'T'
