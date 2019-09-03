"""shop models module."""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from customer.models import Customer


class Saloon(models.Model):
    """saloo django model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=60, blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        """str method for Saloon model"""
        return f'{self.user.username} Saloon'

    def _get_user_full_name(self):
        """prpety method for Saloon model"""
        return '%s %s' % (self.user.first_name, self.user.last_name)

    user_full_name = property(_get_user_full_name)


class TimeSlot(models.Model):
    """time slot django model."""
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        """str method for TimeSlot model"""
        return f'{self.time.strftime("%Y-%m-%d %H:%M")} - { self.saloon }'


class Reservation(models.Model):
    """reservation django model"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        """str method for Reservation model"""
        return f'{self.customer.user.username} - { self.time_slot.saloon }'


class Review(models.Model):
    """reservation django model"""
    reservation = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        """str method for Reservation model"""
        return f'{self.reservation.customer.username} review'
