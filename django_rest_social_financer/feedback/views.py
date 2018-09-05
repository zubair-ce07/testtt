from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import  Http404
from  rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics

from .serializers import FeedbackModelSerializer
from accounts.models import UserProfile
from accounts import permissions as local_permissions

class PostFeedbackView(APIView):
    serializer_class = FeedbackModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isPair)

    def post(self, request, pk, format='json',):
        pair_user = get_object_or_404(UserProfile, pk=pk)
        self.check_object_permissions(request, pair_user)
        serializer = FeedbackModelSerializer(instance=pair_user,
                                             data=request.data,
                                             context={'by_user' : request.user.id})
        if serializer.is_valid():
            feedback = serializer.save()
            return redirect(reverse('accounts:home')) if feedback else Http404
