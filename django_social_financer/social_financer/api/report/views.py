from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from . import serializers
from accounts.models import UserProfile
from accounts import permissions as local_permissions


class PostReportView(APIView):
    serializer_class = serializers.ReportModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isPair)

    def post(self, request, format='json'):
        print(self.request.data.get('input', {}))
        pair_user = get_object_or_404(UserProfile, pk=self.request.data.get('input', {}).get('id', -1))
        serializer = serializers.ReportModelSerializer(instance=pair_user,
                                           data=request.data.get('input'),
                                           context={'by_user': self.request.user.id})
        if serializer.is_valid():
            report = serializer.save()
            if report:
                return Response({'detail' : 'Success'}, status=status.HTTP_200_OK)
        return Response({'detail' : 'Failiure', status:status.HTTP_500_INTERNAL_SERVER_ERROR})




class ViewReports(APIView):
    serializer_class = serializers.ViewReportsSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isAdmin)
    def get(self, request, pk):
        serializer = serializers.ViewReportsSerializer(instance=request.user.userprofile)
        return Response(serializer.data)
