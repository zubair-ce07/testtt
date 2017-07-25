from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import UserProfile, DateTime

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


@admin.register(DateTime)
class DateTime(admin.ModelAdmin):
    list_display = ('datetime', 'timezone')
