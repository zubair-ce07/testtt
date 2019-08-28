from django.contrib import admin

from .models import Requests, RequestFiles, Offers

admin.site.register(Requests)
admin.site.register(RequestFiles)
admin.site.register(Offers)
