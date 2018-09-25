from rest_framework.views import APIView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes, api_view

from . import serializers
from api.renderers import UserJSONRenderer
from accounts.models import UserProfile, PairHistory, Category
from accounts import constants, helpers, permissions as local_permissions
from feedback.models import Feedback



class PostFeedbackView(APIView):
    serializer_class = serializers.FeedbackModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isPair)

    def post(self, request, format='json',):
        print(request.data['input'])
        pair_user = get_object_or_404(UserProfile, pk=request.data.get('input', {}).get('id', -1))
        self.check_object_permissions(request, pair_user)
        serializer = serializers.FeedbackModelSerializer(instance=pair_user,
                                             data=request.data.get('input', {}),
                                             context={'by_user' : request.user.id})
        if serializer.is_valid():
            feedback = serializer.save()
            if feedback:
                return Response({'detail' : 'Feedback Submission Successful'}, status=status.HTTP_200_OK)
        return Response({'detail' : 'feedback not submitted'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#
class GetFeedbackView(generics.ListAPIView):
    serializer_class = serializers.FeedbackModelSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Feedback.objects.filter(given_to_user=self.request.query_params.get('id', -1))
