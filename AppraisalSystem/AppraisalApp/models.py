from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

COMPETENCY_RANGE = [MaxValueValidator(10), MinValueValidator(1)]
USER_TYPES = [(1, "CEO"), (2, "Manager"), (3, "Worker"), ]


class Employee(AbstractUser):
    employee_type = models.IntegerField(choices=USER_TYPES, blank=True, default=3)
    reports_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Employee'


class Feedback(models.Model):
    from_user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='given_feedbacks')
    to_user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='feedbacks')
    publishing_date = models.DateTimeField(auto_now_add=True)


class Competency(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, unique=True)
    comment = models.TextField(max_length=500, blank=True)
    team_work = models.IntegerField(default=1, validators=COMPETENCY_RANGE)
    leadership = models.IntegerField(default=1, validators=COMPETENCY_RANGE)
