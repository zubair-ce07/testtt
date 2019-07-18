from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    last_modified = models.DateTimeField(auto_now=True)
