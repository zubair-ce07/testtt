from rest_framework.permissions import BasePermission, SAFE_METHODS


class isAdminOrBuyerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_buyer


class isSameBuyer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user
