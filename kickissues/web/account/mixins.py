from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin


class IssueOwnerPermissionMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied("You Dont Have Access to this Page")
        return obj
