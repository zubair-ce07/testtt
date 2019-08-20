from django.contrib import admin
from .models import User

# registered custom used model with the admin app

admin.site.site_header = "User Profiles"
admin.site.site_title = "User Profiles"


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'gender']
    list_filter = ('gender', 'email')


admin.site.register(User, UserAdmin)
