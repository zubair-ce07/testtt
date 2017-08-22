from django.contrib import admin
from .models import User, Comment, Like, Post, FollowRelation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'get_name', 'email', 'date_of_birth',)# 'avatar',)
    search_fields = ('first_name', 'last_name', 'username')
    fields = ('first_name', 'last_name', 'username', 'email',
              'date_of_birth', 'avatar', 'bio')

    def get_name(self, instance):
        return instance.first_name+' '+instance.last_name


@admin.register(FollowRelation)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_user_name', 'get_follower_name')

    def get_user_name(self, instance):
        return instance.user.username
    get_user_name.short_description = 'User'

    def get_follower_name(self, instance):
        return instance.follower.username
    get_follower_name.short_description = 'Follower'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'user', 'created_at', 'image')
    search_fields = ('text', 'user__username')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'user', 'post', 'get_username',
                    'timestamp')
    search_fields = ('user__username', 'text')
    list_filter = ('timestamp',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    def get_username(self, obj):
        return obj.post.user.username
    get_username.short_description = 'Post Author'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post', 'get_username', 'timestamp')
    search_fields = ('user__username', 'post__text', 'post__username')
    list_filter = ('timestamp',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    def get_username(self, obj):
        return obj.post.user.username
    get_username.short_description = 'Post Author'

