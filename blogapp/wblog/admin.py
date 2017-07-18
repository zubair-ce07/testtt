from django.contrib import admin
from .models import UserInfo, Blog, Comment

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Comment)
