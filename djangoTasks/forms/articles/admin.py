from django.contrib import admin

from articles.models import *


class ArticlesAdmin(admin.ModelAdmin):

    fields = ('title', 'category_name', 'writer', 'publication_date')
    list_display = ('title', 'category_name', 'writer', 'publication_date')
    search_fields = ('title', 'tags')
    list_filter = ('writer', )

admin.site.register(Articles, ArticlesAdmin)
