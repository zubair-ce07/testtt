from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Feedbacks(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    cell_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    age = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    nps = models.IntegerField(blank=True, null=True)
    satisfaction_level = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey(Department, null=True)
    store = models.ForeignKey(Store, null=True)

    def __str__(self):
        return self.name
