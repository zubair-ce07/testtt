from django.contrib import admin
from .models import User, Comment, Like, Post, FollowRelation


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'get_name', 'email', 'date_of_birth', 'avatar',)
    search_fields = ('first_name', 'last_name', 'username')
    ordering = ('pk',)
    fields = ('first_name', 'last_name', 'username', 'email',
              'date_of_birth', 'avatar', 'bio')
    # filter_horizontal = ('following',)

    def get_name(self, instance):
        return instance.first_name+' '+instance.last_name


class FollowersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_user_name', 'get_follower_name')

    def get_user_name(self, instance):
        return instance.user.username
    get_user_name.short_description = 'User'

    def get_follower_name(self, instance):
        return instance.follower.username
    get_follower_name.short_description = 'Follower'


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'user', 'created_at', 'image')
    search_fields = ('text', 'user__username')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('user',)


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


class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post', 'get_username', 'timestamp')
    search_fields = ('user__username', 'post__text', 'post__username')
    list_filter = ('timestamp',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    def get_username(self, obj):
        return obj.post.user.username
    get_username.short_description = 'Post Author'


admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(FollowRelation, FollowersAdmin)
