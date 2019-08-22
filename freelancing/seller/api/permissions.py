from rest_framework.permissions import BasePermission, SAFE_METHODS


class isAdminOrSellerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_seller


class isSameSeller(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user
