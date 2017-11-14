from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Invite, Tutor
from django.utils.timezone import now


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


class CanGiveFeedback(BasePermission):

    def has_object_permission(self, request, view, obj):
        tutor_object = get_object_or_404(Tutor, username=obj.username)
        invite_object = get_object_or_404(Invite, tutor_id=tutor_object.id, student_id=request.user.id)
        if invite_object.accepted:
            return (now() - invite_object.accepting_time).total_seconds() > 200
        return False
