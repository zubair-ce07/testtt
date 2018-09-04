from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

from accounts.models import UserProfile

# Create your models here.
class Report(models.Model):
    reporting_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='submitted_report')
    reported_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_reports')
    category_types = (
        ('IL', 'Inappropriate language'),
        ('FA', 'Fake account'),
        ('MS', 'Misuse of service'),
        ('OT', 'Other')
    )
    category = models.CharField(max_length=2, choices=category_types)
    comments = models.TextField(max_length= 500)
    date_logged = models.DateTimeField(default=datetime.now, blank=True)
