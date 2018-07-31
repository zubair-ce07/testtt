from django.contrib import admin
from .models import Article
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'description', 'category', 'content']
    list_filter = ['category']
    search_fields = ['title']


