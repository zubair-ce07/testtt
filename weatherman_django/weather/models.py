"""
this module contains the Models of this django app
"""
from django.db import models
from django.utils import timezone


class WeatherCharacteristics(models.Model):
    """
    Weather charactersitics class
    """
    max_value = models.FloatField(null=True)
    mean_value = models.FloatField(null=True)
    min_value = models.FloatField(null=True)


class City(models.Model):
    """
    City Model class
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Weather(models.Model):
    """
    Weahter Model
    """
    date = models.DateField(default=timezone.now)
    temperature = models.OneToOneField(WeatherCharacteristics, on_delete=models.CASCADE,
                                       related_name='+')
    dew_point = models.OneToOneField(WeatherCharacteristics, on_delete=models.CASCADE,
                                     related_name='+')
    humidity = models.OneToOneField(WeatherCharacteristics, on_delete=models.CASCADE,
                                    related_name='+')
    sea_pressure = models.OneToOneField(WeatherCharacteristics, on_delete=models.CASCADE,
                                        related_name='+')
    visibility = models.OneToOneField(WeatherCharacteristics, on_delete=models.CASCADE,
                                      related_name='+')
    wind = models.OneToOneField(WeatherCharacteristics, on_delete=models.CASCADE,
                                related_name='+')
    max_gust_speed = models.PositiveSmallIntegerField(null=True)
    precipitation = models.FloatField(null=True)
    cloud_cover = models.PositiveSmallIntegerField(null=True)
    events = models.CharField(max_length=150, null=True)
    wind_dir_degrees = models.SmallIntegerField(null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
