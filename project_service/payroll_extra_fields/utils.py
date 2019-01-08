'''
Holds all utility functions for payroll app
'''
from xmlrpc import client as xmlrpc_client
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from payroll.constants import (
    DB, LIMIT, OFFSET, PASSWORD, URL, USERNAME,
    ALLOWANCE, BASIC, DEDUCTION, NET
)
from payroll.fields import (
    PAYSLIPS_SUMMARY, PAYSLIP_DETAILS, PAYSLIP_LINE_DETAILS, EMPLOYEES_SUMMARY
)
from payroll.exceptions import OdooBadCallException
from .models import Payslip
from .serializers import PayslipSerializer


class OdooAuthentication:
    '''
    Odoo authentication (user id and models retrival)
    '''
    __uid = None
    __models = None

    def __init__(self):
        if not self.__uid:
            self.get_uid()
        if not self.__models:
            self.get_models()

    @staticmethod
    def get_uid():
        '''
        Request user_id from odoo external api
        '''
        if not OdooAuthentication.__uid:
            common = xmlrpc_client.ServerProxy('{}/xmlrpc/2/common'.format(URL))
            OdooAuthentication.__uid = common.authenticate(DB, USERNAME, PASSWORD, {})
        return OdooAuthentication.__uid

    @staticmethod
    def get_models():
        '''
        Request models from odoo external api
        '''
        if not OdooAuthentication.__models:
            OdooAuthentication.__models = xmlrpc_client.ServerProxy('{}/xmlrpc/2/object'.format(URL))
        return OdooAuthentication.__models

    @staticmethod
    def get_uid_and_models():
        '''
        Return user_id and models
        '''
        return (OdooAuthentication.get_uid(), OdooAuthentication.get_models())


class OdooPayslipLine:
    @staticmethod
    def __execute_kw(method, *args):
        uid, models = OdooAuthentication.get_uid_and_models()

        try:
            return models.execute_kw(DB, uid, PASSWORD, 'hr.payslip.line', method, *args)
        except xmlrpc_client.Fault as error:
            raise OdooBadCallException(error.faultString)

    @staticmethod
    def filter(**kwargs):
        '''
        Method to filter payslips
        '''
        offset = kwargs.pop('offset') if 'offset' in kwargs else OFFSET
        limit = kwargs.pop('limit') if 'limit' in kwargs else LIMIT

        params = [[key, 'in', kwargs[key]] for key in kwargs]

        return OdooPayslipLine.__execute_kw('search_read', [params], {
            'fields': PAYSLIP_LINE_DETAILS, 'offset': offset, 'limit':  limit
        })

    @staticmethod
    def update(id=None, data=None):
        OdooPayslipLine.__execute_kw('write', [[id], data])

    @staticmethod
    def delete(ids):
        OdooPayslipLine.__execute_kw('unlink', [ids])


class OdooPayslip:
    '''
    Make payslip crud request to odoo
    '''
    @staticmethod
    def __execute_kw(method, *args):
        uid, models = OdooAuthentication.get_uid_and_models()

        try:
            return models.execute_kw(DB, uid, PASSWORD, 'hr.payslip', method, *args)
        except xmlrpc_client.Fault as error:
            raise OdooBadCallException(error.faultString)

    @staticmethod
    def __update_payslip_line(id, data):
        OdooPayslip.__execute_kw('write', [[id], data])

        total_amount = 0
        for payslip_line in OdooPayslipLine.filter(slip_id=[id]):
            if payslip_line['category_id'][0] in [BASIC, ALLOWANCE]:
                total_amount += payslip_line['amount']
            elif payslip_line['category_id'][0] == DEDUCTION:
                total_amount -= payslip_line['amount']
            elif payslip_line['category_id'][0] == NET:
                net_category_id = payslip_line['id']

        OdooPayslipLine.update(id=net_category_id, data={'amount': total_amount})

    @staticmethod
    def get(**kwargs):
        '''
        Method to get single payslip
        '''
        params = [[key, '=', kwargs[key]] for key in kwargs]

        payslips = OdooPayslip.__execute_kw('search_read', [params], {'fields': PAYSLIP_DETAILS})

        if payslips and len(payslips) == 1:
            # Get fields from our end
            payslip = Payslip.objects.get(odoo_payslip_id=payslips[0]['id'])
            payslip_extra_fields = PayslipSerializer(payslip).data
            payslips[0].update(payslip_extra_fields)
            return payslips[0]
        elif len(payslips) > 1:
            raise MultipleObjectsReturned
        else:
            raise ObjectDoesNotExist

    @staticmethod
    def filter(**kwargs):
        '''
        Method to filter payslips
        '''
        offset = kwargs.pop('offset') if 'offset' in kwargs else OFFSET
        limit = kwargs.pop('limit') if 'limit' in kwargs else LIMIT

        params = [[key, '=', kwargs[key]] for key in kwargs]

        odoo_payslips = OdooPayslip.__execute_kw('search_read', [params], {
            'fields': PAYSLIPS_SUMMARY, 'offset': offset, 'limit':  limit
        })

        odoo_payslip_ids = list(map(lambda payslip: payslip['id'], odoo_payslips))

        payslips = Payslip.objects.filter(odoo_payslip_id__in=odoo_payslip_ids)
        payslips = PayslipSerializer(payslips, many=True).data

        for odoo_payslip in odoo_payslips:
            # Searching for payslip
            payslip = next(
                (payslip for payslip in payslips if payslip['odoo_payslip_id'] == odoo_payslip['id']), False
            )
            if payslip:
                odoo_payslip.update(payslip)
        return odoo_payslips

    @staticmethod
    def create(data=None):
        '''
        Method to create employee payslip
        '''
        payslip_data = {
            'line_ids': data.pop('line_ids') if 'line_ids' in data else []
        }
        description = data.pop('description') if 'description' in data else ''
        payslip_id = OdooPayslip.__execute_kw('create', [data])

        # Adding extra fields' data
        payslip_serializer = PayslipSerializer(data={'description': description,
                                                     'odoo_payslip_id': payslip_id})
        if payslip_serializer.is_valid():
            payslip_serializer.save()

            if OdooPayslip.__execute_kw('compute_sheet', [[payslip_id]]):
                return OdooPayslip.update(id=payslip_id, data=payslip_data)

            return OdooPayslip.get(id=payslip_id)
        OdooPayslip.delete(ids=[payslip_id])
        raise OdooBadCallException(payslip_serializer.errors)

    @staticmethod
    def update(id=None, data=None):
        '''
        Method to update employee payslip
        '''
        # Updating fields on our db
        if 'description' in data:
            description = data.pop('description')
            payslip_serializer = PayslipSerializer(data={'description': description}, partial=True,
                                                   instance=Payslip.objects.get(odoo_payslip_id=id))
            if payslip_serializer.is_valid(raise_exception=True):
                payslip_serializer.save()

        if 'line_ids' in data:
            OdooPayslip.__update_payslip_line(id, data)
        else:
            OdooPayslip.__execute_kw('write', [[id], data])

        return OdooPayslip.get(id=id)

    @staticmethod
    def delete(ids=None):
        '''
        Method to delete payslips
        '''
        OdooPayslip.__execute_kw('unlink', [ids])

        Payslip.objects.filter(odoo_payslip_id__in=ids).delete()

    @staticmethod
    def bulk_update(ids=None, data=None):
        '''
        Method to bulk update payslips data
        '''
        OdooPayslip.__execute_kw('write', [ids, data])


class OdooEmployee:

    @staticmethod
    def __execute_kw(method, *args):
        uid, models = OdooAuthentication.get_uid_and_models()

        try:
            return models.execute_kw(DB, uid, PASSWORD, 'hr.employee', method, *args)
        except xmlrpc_client.Fault as error:
            raise OdooBadCallException(error.faultString)

    @staticmethod
    def compute_sheet(id=None):
        return OdooEmployee.__execute_kw('compute_sheet', [[id]])

    @staticmethod
    def filter(**kwargs):
        '''
        Method to filter payslips
        '''
        offset = kwargs.pop('offset') if 'offset' in kwargs else OFFSET
        limit = kwargs.pop('limit') if 'limit' in kwargs else LIMIT

        params = [[key, '=', kwargs[key]] for key in kwargs]

        return OdooEmployee.__execute_kw('search_read', [params], {
            'fields': EMPLOYEES_SUMMARY, 'offset': offset, 'limit':  limit
        })
