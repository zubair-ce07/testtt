from django.contrib import admin

# Register your models here.
from .models import Requests, RequestFiles
admin.site.register(Requests)
admin.site.register(RequestFiles)
