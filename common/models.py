from django.db import models
from teams.managers import SoftDeleteManager


# add to common file
class SoftDeleteModelMixin(models.Model):
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    valid_objects = SoftDeleteManager()

    class Meta:
        abstract = True
