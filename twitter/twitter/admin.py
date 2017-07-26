from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group

from twitter.models import User, Tweet, News


class UserAdmin(AuthUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    filter_horizontal = ('followers',)

    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('followers', {'fields': ('followers',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'content',)}),
        ('Media', {'fields': ('image', )})
    )

    def save_model(self, request, obj, form, change):
        obj.get_publisher = request.user
        super(NewsAdmin, self).save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Tweet)

admin.site.unregister(Group)
