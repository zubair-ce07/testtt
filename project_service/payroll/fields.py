'''
Fields to retrieve/send when calling Odoo external API
'''

PAYSLIPS_SUMMARY = [
    'number', 'employee_id', 'name', 'date_from',
    'date_to', 'state', 'company_id', 'payslip_run_id'
]

PAYSLIP_DETAILS = [
    'number', 'employee_id', 'name', 'date_from',
    'date_to', 'state', 'company_id', 'payslip_run_id',
    'payslip_count', 'contract_id', 'struct_id', 'credit_note',
    'worked_days_line_ids', 'input_line_ids', 'line_ids',
    'details_by_salary_rule_category', 'paid', 'display_name'
]
