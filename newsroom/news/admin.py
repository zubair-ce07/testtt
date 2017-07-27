from django.contrib import admin
from .models import Newspaper, News, Scrapper, NewsSource, Category


admin.site.register(Newspaper)
admin.site.register(Scrapper)
admin.site.register(Category)
admin.site.register(NewsSource)
admin.site.register(News)
