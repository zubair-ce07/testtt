from django.contrib import admin
from .models import CustomUser, Task


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'city')
    search_fields = ('username', 'first_name', 'last_name')
    fields = ('last_name', 'first_name', 'username', 'email', 'city', 'profile_picture', 'height_field', 'width_field')


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task)
