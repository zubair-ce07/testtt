from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Product, Order

class CustomUserAdmin(UserAdmin):
    """ To make changings in Custom User of Admin side """
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', 'phone', 'address', 'type', 'status'),
        }),
    )
    form = CustomUserChangeForm
    fieldsets = (
        (('User'), {'fields': ('email', 'phone', 'address', 'type', 'status')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff')})
    )
    model = CustomUser
    list_display = ['email', 'username', 'type', 'status']
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Order)
