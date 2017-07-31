from django.contrib import admin


from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'supervisor')


admin.site.register(Profile, ProfileAdmin)
