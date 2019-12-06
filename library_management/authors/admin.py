from django.contrib import admin

from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Bio', {'fields': ['username', 'first_name', 'last_name']}),
        ('Contact', {'fields': ['phone', 'email']}),
    ]
    list_display = ['id', 'username', 'first_name']
