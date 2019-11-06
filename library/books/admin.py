"""Module for Books admin."""
from django.contrib import admin
from .models import Book, IssueBook, RequestBook

class BooksAdmin(admin.ModelAdmin):
    """Display for Books admin."""
    list_display = ('title', 'author_name')

admin.site.register(Book, BooksAdmin)
admin.site.register(IssueBook)
admin.site.register(RequestBook)

