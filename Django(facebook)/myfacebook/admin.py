from django.contrib import admin

from .models import UserFollowers, UserStatus

admin.site.register(UserFollowers)
admin.site.register(UserStatus)
