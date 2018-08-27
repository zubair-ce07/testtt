from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

from accounts.models import UserProfile

# Create your models here.
class Feedback(models.Model):
    given_by_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_feedback')
    given_to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_feedback')
    star_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5, message='Rating must be between 1-5')])
    comments = models.TextField(max_length=350, blank=True)
    date_logged = models.DateTimeField(default=datetime.now, blank=True)