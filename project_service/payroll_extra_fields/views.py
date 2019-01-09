from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payroll.constants import LIMIT, OFFSET
from payroll.permissions import IsAccountant
from .models import Payslip
from .utils import OdooBadCallException, OdooPayslip
from .serializers import PayslipSerializer


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
                                          limit=request.GET.get('limit') or LIMIT)
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


class ReviewPayslipView(generics.UpdateAPIView):
    '''
    Set Payslip status to review
    '''
    permission_classes = (IsAuthenticated, )

    def partial_update(self, request, pk):
        try:
            payslip = Payslip.objects.get(odoo_payslip_id=pk)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        payslip_serializer = PayslipSerializer(data={'is_reviewed': True}, instance=payslip, partial=True)

        if payslip_serializer.is_valid(raise_exception=True):
            payslip_serializer.save()

            return Response(OdooPayslip.get(id=payslip.odoo_payslip_id), status=status.HTTP_200_OK)


class ConfirmPayslipView(generics.UpdateAPIView):
    '''
    Bulk confirm payslips
    '''
    permission_classes = (IsAuthenticated, )

    def partial_update(self, request, *args, **kwargs):
        payslip_ids = request.data.get('payslip_ids', [])

        if OdooPayslip.bulk_update(ids=payslip_ids, data={'state': 'done'}):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
