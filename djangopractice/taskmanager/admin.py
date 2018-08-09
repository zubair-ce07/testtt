from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from taskmanager.models import CustomUser, Task
from taskmanager.forms import CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        ('User details', {
            'fields': ('username', 'first_name', 'last_name', 'email')
        }),
        ('Extra', {
            'fields': ('bio', 'image', 'birth_date')
        }),
    )
    list_display = ['username', 'id', 'full_name', 'total_tasks']


admin.site.register(Task)
admin.site.register(CustomUser, CustomUserAdmin)
