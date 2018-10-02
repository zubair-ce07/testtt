from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin for User data model.
    """
    list_display = ('user', 'address', 'age')

    model = Profile

    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'


admin.site.register(Profile, ProfileAdmin)
