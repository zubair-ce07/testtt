from django.forms import ModelForm

from .models import Report

class ReportForm(ModelForm):
    class Meta:
        model = Report
        exclude = ['reporting_user', 'reported_user', 'date_logged']