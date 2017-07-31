import json

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().select_related('user')
    serializer_class = EmployeeSerializer


class EmployeeDirectsView(APIView):
    """
    View to list the complete heirarchy of Employees starting from the current Employee
    """

    def get(self, request, pk, *args, **kwargs):
        """
        Returns the directs of the current Employee
        """
        response_dict = {
            'Employee': "",
            'directs': []
        }
        employee = Employee.objects.get(pk=pk)
        directs = Employee.objects.filter(reports_to=employee).all()
        directs = list(map(lambda x: EmployeeSerializer(x).data, directs))
        response_dict['Employee'] = EmployeeSerializer(employee).data
        response_dict['directs'] = directs
        return Response(response_dict, status=status.HTTP_200_OK)
