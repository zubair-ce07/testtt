from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import redirect
from  rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import ReportModelSerializer, ViewReportsSerializer
from accounts.models import UserProfile
from accounts import permissions as local_permissions


class PostReportView(APIView):
    serializer_class = ReportModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isPair)

    def post(self, request, format='json'):
        pair_user = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        serializer = ReportModelSerializer(instance=pair_user,
                                           data=request.data,
                                           context={'by_user': self.request.user.id})
        if serializer.is_valid():
            report = serializer.save()
            return redirect(pair_user.role) if report else Http404

    def get_reverse_url(self, role):
        return 'accounts:my_consumers' if role == 'DN' else 'accounts:home'


class ViewReports(APIView):
    serializer_class = ViewReportsSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isAdmin)
    def get(self, request, pk):
        serializer = ViewReportsSerializer(instance=request.user.userprofile)
        return Response(serializer.data)
