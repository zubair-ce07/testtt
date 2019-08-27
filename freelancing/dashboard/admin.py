from django.contrib import admin

# Register your models here.
from .models import Requests, RequestFiles, Offers
admin.site.register(Requests)
admin.site.register(RequestFiles)
admin.site.register(Offers)
