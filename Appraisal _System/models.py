from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

USER_TYPE_CHOICES = (
        ('admin', 'admin'),
        ('manager', 'manager'),
        ('employee', 'employee'),
        ('none', 'none')
    )

class User(AbstractUser):
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    report_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    user_level = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="none")

class Appraisal(models.Model):
    description = models.TextField()
    comment = models.TextField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='form_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='to_user')
    date = models.DateTimeField(auto_now=True)

class Competence(models.Model):
    decision_making = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    confidence = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    problem_solving = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    appraisal = models.ForeignKey(Appraisal, on_delete=models.CASCADE)
    def __str__(self):
        return f'''(Decision Making - {str(self.decision_making)})
                   (Problem Solving - {str(self.problem_solving)})
                   (Confidence - {str(self.confidence)})'''

