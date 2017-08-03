import json

from django.shortcuts import render

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


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all().select_related('user')
    serializer_class = EmployeeSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class EmployeeDirectsView(APIView):
    """
    View to list the complete heirarchy of Employees starting from the current Employee
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        """
        Returns the directs of the current Employee
        """
        response_dict = {
            'directs': []
        }
        employee = Employee.objects.get(pk=pk)
        directs = Employee.objects.filter(reports_to=employee).all()
        directs = list(map(
            lambda x: EmployeeSerializer(x, context={'request': request}).data,
            directs))
        response_dict['directs'] = directs
        return Response(response_dict, status=status.HTTP_200_OK)
