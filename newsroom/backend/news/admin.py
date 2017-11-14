from django.contrib import admin

from backend.news.models import News, Newspaper, NewsSource, Scrapper


class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "category", "newspaper",)
    list_filter = ("category", "newspaper", "news_source", "sentiment")

admin.site.register(Newspaper)
admin.site.register(Scrapper)
admin.site.register(NewsSource)
admin.site.register(News, NewsAdmin)
