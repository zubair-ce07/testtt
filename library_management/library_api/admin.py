from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Author, Book, Category, CustomUser, Publisher


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username',]


class AuthorInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Book.categories.through
    extra = 1


class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'isbn']}),
        ('Date information', {'fields': ['date_published', 'pages']}),
        ('Categories', {'fields': ['categories']}),
        ('Authors', {'fields': ['authors']}),
        ('Publisher', {'fields': ['publisher']}),
    ]

    # TODO: make inlines work
    # inlines = [AuthorInline, CategoryInline]


class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Bio', {'fields': ['username', 'first_name', 'last_name']}),
        ('Contact', {'fields': ['phone', 'email']}),
    ]


class PublisherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Account Info', {'fields': ['username',]}),
        ('Info', {'fields': ['company_name',]}),
        ('Contact', {'fields': ['phone', 'email', 'website', 'address']}),
    ]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Publisher, PublisherAdmin)
