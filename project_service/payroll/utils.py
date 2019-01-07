'''
Holds all utility functions for payroll app
'''
from xmlrpc import client as xmlrpc_client
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from .constants import (
    DB, LIMIT, OFFSET, PASSWORD, URL, USERNAME,
    ALLOWANCE, BASIC, DEDUCTION, NET
)
from .fields import PAYSLIPS_SUMMARY, PAYSLIP_DETAILS, PAYSLIP_LINE_DETAILS
from .exceptions import OdooBadCallException


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
        # return super().__execute_kw('hr.payslip', method, *args)
        uid, models = OdooAuthentication.get_uid_and_models()

        try:
            return models.execute_kw(DB, uid, PASSWORD, 'hr.payslip', method, *args)
        except xmlrpc_client.Fault as error:
            raise OdooBadCallException(error.faultString)

    @staticmethod
    def __update_payslip_line(id, data):
        payslip_line_ids = list(
            map(lambda line: line['id'], OdooPayslipLine.filter(slip_id=[id], code=['LN', 'Bonus']))
        )
        OdooPayslipLine.delete(payslip_line_ids)
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

        return OdooPayslip.__execute_kw('search_read', [params], {
            'fields': PAYSLIPS_SUMMARY, 'offset': offset, 'limit':  limit
        })

    @staticmethod
    def create(data=None):
        '''
        Method to create employee payslip
        '''
        payslip_data = {
            'line_ids': data.pop('line_ids') if 'line_ids' in data else []
        }
        payslip_id = OdooPayslip.__execute_kw('create', [data])

        if OdooPayslip.__execute_kw('compute_sheet', [[payslip_id]]):
            return OdooPayslip.update(id=payslip_id, data=payslip_data)

        return OdooPayslip.get(id=payslip_id)

    @staticmethod
    def update(id=None, data=None):
        '''
        Method to update employee payslip
        '''
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
