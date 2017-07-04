from django.contrib import admin
from .models import User, Comment, Like, Post


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')
    search_fields = ('name', 'username')

admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)
