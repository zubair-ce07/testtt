"""
Contains the permission classes for API.
"""
from rest_framework.permissions import BasePermission

from accounts.models import UserProfile
from .models import Saloon, Feedback, Appointment


class IsUserASaloonOwner(BasePermission):
    def has_permission(self, request, view):
        """
        Using user_type checks that either user is a saloon owner.
        """
        try:
            UserProfile.objects.get(user_type='o', user=request.user)
        except UserProfile.DoesNotExist:
            return False
        return True


class IsUserACustomer(BasePermission):
    def has_permission(self, request, view):
        """
        Using user_type checks that either user is a saloon owner.
        """
        try:
            UserProfile.objects.get(user_type='c', user=request.user)
        except UserProfile.DoesNotExist:
            return False
        return True


class CanMarkFeedback(BasePermission):
    def has_permission(self, request, view):
        """
        Checks that either a feedback by a specific customer for a specific saloon existed or not
        if existed, he can't give feedback again.
        """
        feedback = Feedback.objects.filter(saloon__id=view.kwargs['pk'], user=request.user)
        if feedback:
            return False
        return True


class CanUpdateUserProfile(BasePermission):
    def has_permission(self, request, view):
        """
        Checks that if user is an owner or a customer, he can update his profile.
        """
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.user_type == 'e':
                return False
            return True
        except UserProfile.DoesNotExist:
            return False


class CanAddEmployee(BasePermission):
    def has_permission(self, request, view):
        """
        Checks that if a user is the owner of the saloon, he can add employees to that saloon.
        """
        try:
            Saloon.objects.get(pk=view.kwargs['pk'], owner=request.user)
            return True
        except Saloon.DoesNotExist:
            return False


class CanProcessAppointment(BasePermission):
    def has_permission(self, request, view):
        """
        Checks that the saloon owner can only process the appointments of his own saloon.
        """
        try:
            Appointment.objects.get(id=view.kwargs['pk'], saloon__owner=request.user)
            return True
        except Appointment.DoesNotExist:
            return False


class CanCancelAppointmet(BasePermission):

    def has_permission(self, request, view):
        """
        Checks that a customer can only cancel his appointments.
        """
        try:
            Appointment.objects.get(id=view.kwargs['pk'], customer=request.user)
            return True
        except Appointment.DoesNotExist:
            return False
