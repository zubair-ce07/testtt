from django.db import models


# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=200)


class Semester(models.Model):
    name = models.IntegerField(default=0)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=200)
    credit_hour = models.FloatField()
    code = models.CharField(max_length=10)
    detail = models.CharField(max_length=300)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
