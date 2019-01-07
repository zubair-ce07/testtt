from xmlrpc import client as xmlrpc_client

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import DB, LIMIT, OFFSET
from .fields import PAYSLIPS_SUMMARY, PAYSLIP_DETAILS
from .permissions import IsAccountant
from .utils import OdooAuthentication, OdooBadCallException, OdooPayslip


class EmployeesPayrollViewset(viewsets.ViewSet):
    '''
    Viewset for retrieving, listing, and creating employees' payslips
    '''
    permission_classes = (IsAuthenticated, IsAccountant)

    def retrieve(self, request, pk=None):
        '''
        Get complete employee payslip details
        '''
        try:
            payslip_id = int(pk)
        except (TypeError, ValueError):
            return Response({'error': '`{}` is not a valid payroll id'.format(pk)},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            payslip = OdooPayslip.get(id=payslip_id)
        except (ObjectDoesNotExist, MultipleObjectsReturned, OdooBadCallException):
            return Response({'error': 'Error fetching content'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(payslip, status=status.HTTP_200_OK)

    def list(self, request):
        '''
        List all employees' payslips
        '''
        try:
            payslips = OdooPayslip.filter(offset=request.GET.get('offset') or OFFSET,
                                          limit=request.GET.get('limit') or LIMIT, state='done')
        except OdooBadCallException:
            return Response({'error': 'Error fetching content'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(payslips, status=status.HTTP_200_OK)

    def create(self, request):
        '''
        Create a payslip for employee
        '''
        payslip_data = request.data

        try:
            payslip = OdooPayslip.create(data=payslip_data)
        except OdooBadCallException:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(payslip, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        '''
        Update employee payslip
        '''
        try:
            payslip_id = int(pk)
        except (TypeError, ValueError):
            return Response({'error': '`{}` is not a valid payroll id'.format(pk)},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            payslip = OdooPayslip.update(id=payslip_id, data=request.data)
        except OdooBadCallException:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(payslip, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        '''
        Deletes an employee paylip
        '''
        try:
            payroll_id = int(pk)
        except (TypeError, ValueError):
            return Response({'error': '`{}` is not a valid payroll id'.format(pk)},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            OdooPayslip.delete(ids=[payroll_id])
        except OdooBadCallException:
            return Response({'error': 'Error deleting content'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
