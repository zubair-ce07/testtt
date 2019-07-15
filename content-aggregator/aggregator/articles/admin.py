from django.contrib import admin
from .models import Website, Article, Author

admin.site.register(Website)
admin.site.register(Author)
admin.site.register(Article)
