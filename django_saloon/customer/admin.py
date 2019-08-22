from django.contrib import admin
from .models import Customer, SaloonUser
# Register your models here.

admin.site.register(SaloonUser)
admin.site.register(Customer)
