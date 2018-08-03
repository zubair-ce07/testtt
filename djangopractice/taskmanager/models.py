from datetime import datetime, timedelta
from django.conf import settings
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    due_date = models.DateField('Due Date',
                                default=datetime.now()+timedelta(days=7))

    def __str__(self):
        return "Title :" + self.title

