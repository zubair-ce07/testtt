from django.db import models


class Payslip(models.Model):
    odoo_payslip_id = models.IntegerField(unique=True)
    description = models.TextField(blank=False, null=False)
    is_reviewed = models.BooleanField(default=False)
