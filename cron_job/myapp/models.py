from django.db import models


class DateTimeModel(models.Model):
    now = models.DateTimeField()
    timezone = models.TextField(max_length=30)

    # def __unicode__(self):
    #     return self.now
