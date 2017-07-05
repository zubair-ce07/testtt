from django.contrib import admin
from .models import User, Comment, Like, Post


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')
    search_fields = ('name', 'username')
    ordering = ('pk',)
    # fields = ('email', 'username', 'password', 'name', 'following', 'followed_by')
    filter_horizontal = ('following', 'followed_by',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'user', 'created_at')
    search_fields = ('text', 'user__username')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'user', 'post', 'get_username', 'comment_timestamp')
    search_fields = ('user__username', 'text')
    list_filter = ('comment_timestamp',)
    date_hierarchy = 'comment_timestamp'
    ordering = ('-comment_timestamp',)
    # raw_id_fields = ('user', 'post')

    def get_username(self, obj):
        return obj.post.user.username
    get_username.short_description = 'Post Author'


class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post', 'get_username', 'like_timestamp')
    search_fields = ('user__username', 'post__text', 'post__user__username')
    list_filter = ('like_timestamp',)
    date_hierarchy = 'like_timestamp'
    ordering = ('-like_timestamp',)
    # raw_id_fields = ('user', 'post')

    def get_username(self, obj):
        return obj.post.user.username
    get_username.short_description = 'Post Author'

admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Post, PostAdmin)
