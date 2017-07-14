from rest_framework.permissions import BasePermission
from .models import Task, CustomUser


class IsUserOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if isinstance(obj, Task):
            return obj.user == request.user
        return obj.user == request.user
