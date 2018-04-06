from django.db import models
from django.contrib.auth.models import User


class Employee(User):
    user_type = models.CharField(max_length=100)


class Project(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    budget = models.IntegerField()

class Bids(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    cover_letter = models.CharField(max_length=500)
    status = models.CharField(max_length=100, default="Pending")
    bider_user_id = models.IntegerField()
    project_status = models.CharField(max_length=100, default="Not Hired")

