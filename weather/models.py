from django.db import models


class WeatherModel(models.Model):
    '''
    Model for weather data from madrid.csv file
    '''
    date = models.DateField()
    max_temp = models.FloatField(default=0, null=True, blank=True)
    mean_temp = models.FloatField(default=0, null=True, blank=True)
    min_temp = models.FloatField(default=0, null=True, blank=True)
    max_dew = models.FloatField(default=0, null=True, blank=True)
    mean_dew = models.FloatField(default=0, null=True, blank=True)
    min_dew = models.FloatField(default=0, null=True, blank=True)
    max_humidity = models.FloatField(default=0, null=True, blank=True)
    mean_humidity = models.FloatField(default=0, null=True, blank=True)
    min_humidity = models.FloatField(default=0, null=True, blank=True)
    max_sea_pressure = models.FloatField(default=0, null=True, blank=True)
    mean_sea_pressure = models.FloatField(default=0, null=True, blank=True)
    min_sea_pressure = models.FloatField(default=0, null=True, blank=True)
    max_visibility = models.FloatField(default=0, null=True, blank=True)
    mean_visibility = models.FloatField(default=0, null=True, blank=True)
    min_visibility = models.FloatField(default=0, null=True, blank=True)
