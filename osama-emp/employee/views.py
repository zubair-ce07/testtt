import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import permissions


from .models import Employee
from .serializers import EmployeeSerializer
from .permissions import IsSelf, IsDirect


class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all().select_related('user')
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,
                          permissions.IsAdminUser,)
    lookup_field = 'username'


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all().select_related('user')
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'


class EmployeeDirectsView(APIView):
    """
    View to list the complete heirarchy of Employees starting from the current Employee
    """
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, username, *args, **kwargs):
        """
        Returns the directs of the current Employee
        """
        response_dict = {
            'directs': []
        }
        employee = Employee.objects.get(username=username)
        directs = Employee.objects.filter(reports_to=employee)
        directs = list(map(
            lambda x: EmployeeSerializer(x, context={'request': request}).data,
            directs))
        response_dict['directs'] = directs
        return Response(response_dict, status=status.HTTP_200_OK)
