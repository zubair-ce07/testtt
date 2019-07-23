from django.contrib import admin
from .models import Website, Article, Author, Comment

admin.site.register(Website)
admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Comment)
