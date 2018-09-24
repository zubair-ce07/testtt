from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOfEmplyee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.to_user.reports_to == request.user

