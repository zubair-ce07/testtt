from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User, Comment, Like, Post
from instagram.forms import SignUpForm, LoginForm
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'get_name', 'email', 'avatar', 'bio')
    search_fields = ('first_name', 'last_name', 'username')
    ordering = ('pk',)
    fields = ('first_name', 'last_name', 'username', 'email', 'password', 'date_of_birth', 'avatar', 'bio', 'following')
    filter_horizontal = ('following',)

    def get_name(self, instance):
        return instance.first_name+' '+instance.last_name

    # form = LoginForm
    # add_form = SignUpForm
    #
    # def get_username(self, instance):
    #     return instance.user.username
    #
    # def get_email(self, instance):
    #     return instance.user.email


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'user', 'created_at')
    search_fields = ('text', 'user__user__username')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'user', 'post', 'get_username', 'comment_timestamp')
    search_fields = ('user__user__username', 'text')
    list_filter = ('comment_timestamp',)
    date_hierarchy = 'comment_timestamp'
    ordering = ('-comment_timestamp',)
    # raw_id_fields = ('user', 'post')

    def get_username(self, obj):
        return obj.post.user.username
    get_username.short_description = 'Post Author'


class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post', 'get_username', 'like_timestamp')
    search_fields = ('user__user__username', 'post__text', 'post__user__user__username')
    list_filter = ('like_timestamp',)
    date_hierarchy = 'like_timestamp'
    ordering = ('-like_timestamp',)
    # raw_id_fields = ('user', 'post')

    def get_username(self, obj):
        return obj.post.user.username
    get_username.short_description = 'Post Author'

# user_admin = UserAdmin()
# user_admin.register(User, AuthUserAdmin)

admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Post, PostAdmin)
