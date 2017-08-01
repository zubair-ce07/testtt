import json

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Employee
from .serializers import EmployeeSerializer, ProfileSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().select_related('user')
    serializer_class = EmployeeSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        employee = Employee.objects.get(pk=pk)
        return Response(ProfileSerializer(employee,
                                          context={'request': request}).data,
                        status=status.HTTP_200_OK)


class EmployeeDirectsView(APIView):
    """
    View to list the complete heirarchy of Employees starting from the current Employee
    """

    def get(self, request, pk, *args, **kwargs):
        """
        Returns the directs of the current Employee
        """
        response_dict = {
            'directs': []
        }
        employee = Employee.objects.get(pk=pk)
        directs = Employee.objects.filter(reports_to=employee).all()
        directs = list(map(lambda x: EmployeeSerializer(
            x, context={'request': request}).data, directs))
        response_dict['directs'] = directs
        return Response(response_dict, status=status.HTTP_200_OK)


class EmployeeHeirarchyView(APIView):
    """
    View to list the complete heirarchy of employees under and employee
    """

    def get_directs(self, employee):
        directs = Employee.objects.filter(reports_to=employee).all()
        return directs

    def get_heirarchy(self, employee):

        pass

    def get(self, request, pk, *args, **kwargs):
        """
        Returns the heirarchy of employees as a Response
        """

        pass
