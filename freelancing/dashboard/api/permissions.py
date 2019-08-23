from rest_framework.permissions import BasePermission, SAFE_METHODS

from ..models import Requests, Offers


class isAdminOrBuyerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_buyer


class isSameBuyer(BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.buyer == request.user


class isSameBuyerRequest(BasePermission):
    def has_object_permission(self, request, view, obj):
        same_buyer_request_file = Requests.objects.filter(
            id=obj.request.id,
            buyer=request.user
        ).exists()
        return same_buyer_request_file or request.user.is_superuser


class isSameBuyerOffer(BasePermission):
    def has_object_permission(self, request, view, obj):
        same_buyer_offer = Requests.objects.filter(
            id=obj.buyer_request.id,
            buyer=request.user
        ).exists()
        return same_buyer_offer or request.user.is_superuser
