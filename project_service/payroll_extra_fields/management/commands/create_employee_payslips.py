from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from dateutil.relativedelta import relativedelta

from payroll_extra_fields.utils import OdooEmployee, OdooPayslip


class Command(BaseCommand):
    help = 'Creates employee payslips'

    def handle(self, *args, **options):
        employees = OdooEmployee.filter(limit=10)
        today = datetime.now()

        payslip_data = {
            "company_id": 1,
            "contract_id": 606,
            "description": "sample description text",
            "credit_note": False,
            "date_from": (today + relativedelta(day=1)).strftime('%Y-%m-%d'),
            "date_to": (today + relativedelta(day=31)).strftime('%Y-%m-%d'),
            "note": False,
            "number": False,
            "payslip_run_id": False,
            "struct_id": 2,
            "worked_days_line_ids": [
                [0, 5, {
                    "code": "WORK100",
                    "contract_id": 606,
                    "name": "Normal Working Days paid at 100%",
                    "number_of_days": 1,
                    "number_of_hours": 8,
                    "sequence": 1
                }]
            ],
            "line_ids": [
                [0, 7, {
                    "amount": 990,
                    "category_id": 4,
                    "code": "LN",
                    "name": "Loan",
                    "quantity": 1,
                    "rate": 100,
                    "salary_rule_id": 12,
                    "sequence": 5
                }], [0, 7, {
                    "amount": 177,
                    "category_id": 2,
                    "code": "Bonus",
                    "name": "Bonus",
                    "quantity": 1,
                    "rate": 100,
                    "salary_rule_id": 13,
                    "sequence": 5
                }]
            ]
        }

        for employee in employees:
            data = dict(payslip_data)
            data['employee_id'] = employee['id']
            data['name'] = 'Salary slip of {} for the month of {}'.format(employee['name'], today.strftime('%B'))

            OdooPayslip.create(data=data)

        self.stdout.write(self.style.SUCCESS('Successfully created payslips'))
