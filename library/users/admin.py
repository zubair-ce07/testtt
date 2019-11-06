"""
Admin Module.

Displays users for Users Administration.
"""
from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """Display for Users admin."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'location', 'age')


admin.site.register(UserProfile, UserProfileAdmin)
