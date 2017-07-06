from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language


class BookInline(admin.TabularInline):
    extra = 0
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    filter_horizontal = ('genre',)
    ordering = ('title',)
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('book','imprint')
                         }),
                 ('Availability', {'fields': ('status', 'due_back', 'borrower')}))
    list_display = ('id', 'book', 'status','borrower', 'due_back')
    list_filter = ('status', 'due_back')


admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
# admin.site.register(BookInstance, BookInstanceAdmin)
# admin.site.register(Author, AuthorAdmin)
admin.site.register(Language)
