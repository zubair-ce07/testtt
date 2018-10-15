import arrow

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

contact_number_validator = RegexValidator(regex=r'^\+?\d{9,15}$',
                                          message='Phone number must be entered in the format:'
                                                  ' +999999999. Up to 15 digits allowed.')


class Saloon(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(validators=[contact_number_validator], max_length=16, blank=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    logo = models.ImageField(upload_to='saloon_logos/', null=True, blank=True, default='images/None/No-image.png')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey('Area', null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('City', null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('saloons:detail', kwargs={'pk': self.id})


class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    attender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='attender', null=True)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=15)
    duration = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('saloons:owner_appointment_detail', kwargs={'pk': self.id, 'saloon_id': self.saloon.id})

    def __str__(self):
        return '{} {}'.format(self.customer, self.saloon)


class Feedback(models.Model):
    rate = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    description = models.TextField()
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateField(default=arrow.get(arrow.utcnow().format('YYYY-MM-DD HH:mm')).datetime)


class SaloonPic(models.Model):
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    path = models.CharField(max_length=100)


class Area(models.Model):
    name = models.CharField(max_length=30)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class City(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{}, {}'.format(self.name, self.country)


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
