"""
this modelue contains the admin related functionality of this django app
"""
from django.contrib import admin
from .models import Weather

admin.site.register(Weather)
