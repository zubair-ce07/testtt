from django.contrib import admin
from reservation.models import Customer, Reservation, Room, Employee


admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Room)
admin.site.register(Reservation)

admin.site.site_header = 'Room Master Administration'
