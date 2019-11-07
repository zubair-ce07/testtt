from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """ To make changings in Custom User of Admin side """
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', 'phone', 'address', 'status', 'role'),
        }),
    )
    form = CustomUserChangeForm
    fieldsets = (
        (('User'), {'fields': ('email', 'phone', 'address', 'type', 'role')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff')})
    )
    model = CustomUser
    list_display = ['email', 'username', 'status', 'role']
admin.site.register(CustomUser, CustomUserAdmin)
