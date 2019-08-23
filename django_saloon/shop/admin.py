from django.contrib import admin
from .models import Saloon, TimeSlot, Reservation

admin.site.register(Saloon)
admin.site.register(TimeSlot)
admin.site.register(Reservation)
