from django.db import models


# Create your models here.

class Institute(models.Model):
    name = models.CharField(max_length=200)


class Program(models.Model):
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)


class Campus(models.Model):
    name = models.CharField(max_length=100)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)


class Department(models.Model):
    name = models.CharField(max_length=100)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)


class Semester(models.Model):
    name = models.IntegerField(default=0)


class Course(models.Model):
    name = models.CharField(max_length=200)
    credit_hour = models.FloatField()
    code = models.CharField(max_length=10)
    detail = models.CharField(max_length=300)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
