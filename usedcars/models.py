from django.db import models


class UsedCars(models.Model):
    make = models.CharField(max_length=25)
    carmodel = models.CharField(max_length=25)
    year = models.CharField(max_length=10)
    millage = models.CharField(max_length=20)
    transmission = models.CharField(max_length=50)
    engine_type = models.CharField(max_length=50)
    reg_city = models.CharField(max_length=50)
    assembly = models.CharField(max_length=10)
    engine_capacity = models.CharField(max_length=20)
    body_type = models.CharField(max_length=20)
    features = models.TextField()
    description = models.TextField()
    image = models.TextField()
