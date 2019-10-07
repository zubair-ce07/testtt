from django.db import models


class DateTime(models.Model):
    time_zone = models.CharField(max_length=50)
    date_and_time = models.DateTimeField(null=False)

    def __str__(self):
        return f'{str(self.date_and_time)}-{self.time_zone}'
