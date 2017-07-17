# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
import models

# Register your models here.


class NewsPaperAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_url', 'crawler_button')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'news_paper', 'source_url')
    list_filter = ('news_paper', 'date')
    search_fields = ('title', 'abstract', 'detail')

    def get_newspaper(self, obj):
        return obj.newspaper.name
    get_newspaper.short_description = 'News Paper'
    get_newspaper.admin_order_field = 'news_paper__name'


admin.site.register(models.NewsPaper, NewsPaperAdmin)
admin.site.register(models.News, NewsAdmin)
