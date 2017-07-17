from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ('id', 'username', 'email',
                    'first_name', 'last_name', 'is_staff')
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password',
                           'first_name', 'last_name',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'confirm_password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')}
         ),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    filter_horizontal = ()


# Register your models here.
admin.site.register(User, CustomUserAdmin)
