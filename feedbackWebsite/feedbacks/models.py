from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return 'Department_%s' % self.name


class Store(models.Model):
    name = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return 'Store_%s' % self.name

class Feedbacks(models.Model):
    created_at = models.DateTimeField()
    name = models.CharField(max_length=254, blank=True, null=True)
    cell_phone = models.CharField(max_length=254, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    age = models.CharField(max_length=254, blank=True, null=True)
    gender = models.CharField(max_length=254, blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    nps = models.IntegerField(blank=True, null=True)
    satisfaction_level = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey(Department, null=True)
    store = models.ForeignKey(Store, null=True)

    def __str__(self):
        return 'Reviewer_%s' % self.name
