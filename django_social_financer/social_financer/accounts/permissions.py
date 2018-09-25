__author__ = 'abdul'
from rest_framework import permissions

from .models import UserProfile


class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class isDonor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.role == UserProfile.DONOR


class isConsumer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.role == UserProfile.CONSUMER


class isPair(permissions.BasePermission):
    message = 'You are not paired with this user. Operation not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.user.userprofile.role == UserProfile.DONOR:
            return obj.id in [user.id for user in request.user.userprofile.pairs.all()]
        elif request.user.userprofile.role == UserProfile.CONSUMER:
            return request.user.userprofile.pair.id == obj.id
        return False
