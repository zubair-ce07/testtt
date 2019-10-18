"""
Admin Module.

Displays users for Users Administration.
"""
from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    """Display for Users admin."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'contact', 'location', 'age')


admin.site.register(UserProfile, UserProfileAdmin)
