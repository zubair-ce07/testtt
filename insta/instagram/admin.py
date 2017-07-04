from django.contrib import admin
from .models import User, Comment, Like, Post


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')
    search_fields = ('name', 'username')


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'created_at')
    search_fields = ('text', 'author__username')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post, PostAdmin)
