from django.contrib import admin
from .models import Book, IssueBook

class BooksAdmin(admin.ModelAdmin):
    """Display for Users admin."""
    list_display = ('title', 'author_name')



admin.site.register(Book, BooksAdmin)
