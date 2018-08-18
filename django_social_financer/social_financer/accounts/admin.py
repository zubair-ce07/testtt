from django.contrib import admin
from django.contrib.auth.models import User, Group

from . import models


class UserInLine(admin.StackedInline):
    model = models.UserProfile
    list_display = ['full_name', 'city', 'country', 'role', 'is_paired']


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'city', 'country', 'role', 'is_paired']
    list_filter = ['userprofile__role', 'userprofile__city', 'userprofile__country']
    inlines = [UserInLine]

    def full_name(self, obj):
        return obj.userprofile.full_name()

    def city(self, obj):
        return obj.userprofile.city

    def country(self, obj):
        return obj.userprofile.country

    def role(self, obj):
        return obj.userprofile.role

    def is_paired(self, obj):
        return obj.userprofile.is_paired()


admin.site.register(models.Category)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

admin.site.site_header = 'Social Financer Admin'
admin.site.index_title = 'Admin'
admin.site.site_title = 'Social Financer'
