from __future__ import unicode_literals

from django.contrib import admin

from .models import DateTime

@admin.register(DateTime)
class DateTimeAdmin(admin.ModelAdmin):
    search_fields = ['date']
