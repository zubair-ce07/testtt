from django.contrib import admin

from .models import Customer
from shop.models import Reservation


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    inlines = [ReservationInline]
