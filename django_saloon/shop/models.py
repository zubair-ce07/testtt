from django.db import models
from django.contrib.auth.models import User

from customer.models import Customer


class Saloon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=60)
    phone_no = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Saloon'

    def _get_user_full_name(self):
        # Returns the person's full name.
        return '%s %s' % (self.user.first_name, self.user.last_name)
    user_full_name = property(_get_user_full_name)


class TimeSlot(models.Model):
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    time = models.DateTimeField()


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
