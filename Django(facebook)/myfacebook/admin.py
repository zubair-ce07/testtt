from django.contrib import admin

from .models import UserFollowers, UserStatus, News, UserProfile

admin.site.register(UserFollowers)
admin.site.register(UserStatus)
admin.site.register(UserProfile)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'date', )
    search_fields = ('author__username', )
    list_filter = ('author', )
