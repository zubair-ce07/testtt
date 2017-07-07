from django.db import models


class Feedbacks(models.Model):
    created_at = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    cell_phone = models.CharField(max_length=254, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    age = models.CharField(max_length=254, blank=True, null=True)
    gender = models.CharField(max_length=254, blank=True, null=True)
    store = models.CharField(max_length=254, blank=True, null=True)
    department = models.CharField(max_length=254, blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    nps = models.CharField(max_length=254, blank=True, null=True)
    satisfaction_level = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return 'Reviewer_%s' % self.name
