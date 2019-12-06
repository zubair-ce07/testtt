from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'isbn']}),
        ('Date information', {'fields': ['date_published', 'pages']}),
        ('Categories', {'fields': ['categories']}),
        ('Authors', {'fields': ['authors']}),
        ('Publisher', {'fields': ['publisher']}),
    ]
    list_display = ['id', 'title', 'isbn']
