"""shop models module."""
from django.db import models
from django.db.models import Sum
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
        """prppety method for Saloon model"""
        return '%s %s' % (self.user.first_name, self.user.last_name)

    @property
    def rating(self):
        """shop rating property"""
        query_set = Review.objects.filter(
            reservation__time_slot__saloon=self)
        rating_count = query_set.count()
        if rating_count:
            total_rating = query_set.aggregate(
                Sum('rating'))['rating__sum'] or 0.00
            return total_rating/rating_count
        return None

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
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        """str method for Reservation model"""
        return f'{self.reservation} - {self.reservation.time_slot.time} review'
