from django.contrib import admin
from .models import Comment, Follow
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text']
    list_filter = ['user', 'text']
    search_fields = ['text']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'player', 'team', 'article']
    list_filter = ['user']
