from django.contrib import admin

from .models import User, Task


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'city')
    search_fields = ('username', 'first_name', 'last_name')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Task)
