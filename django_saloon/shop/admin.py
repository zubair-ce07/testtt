"""shop admin module"""
from django.contrib import admin
from .models import Saloon, TimeSlot, Reservation, Review

admin.site.register(Saloon)
admin.site.register(TimeSlot)
admin.site.register(Reservation)
admin.site.register(Review)
