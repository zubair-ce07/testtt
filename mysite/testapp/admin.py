# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Friend, Post, Audio, Video, Image, Comment, Like

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display = ("username","email","address")

class FriendAdmin(admin.ModelAdmin):
	list_display = ("user","friend")

class PostAdmin(admin.ModelAdmin):
	list_display = ("id","caption","posted_at","user")

class CommentAdmin(admin.ModelAdmin):
	list_display = ("comment","post","user")

class LikeAdmin(admin.ModelAdmin):
	list_display = ("post","user")

admin.site.register(User,UserAdmin)
admin.site.register(Friend,FriendAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Audio)
admin.site.register(Video)
admin.site.register(Image)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Like,LikeAdmin)






