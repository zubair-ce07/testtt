from django.contrib import admin, messages
from django.contrib.auth.models import User, Group
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from . import models
from feedback.models import Feedback


class UserInLine(admin.StackedInline):
    model = models.UserProfile
    list_display = ['full_name', 'city', 'country', 'role', 'is_paired']

class FeedbackInLine(admin.StackedInline):
    model = Feedback
    list_display = ['comments']

class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'city', 'country', 'role', 'is_paired', 'is_activated']
    list_filter = ['userprofile__role', 'userprofile__city', 'userprofile__country']
    search_fields = ['username', 'userprofile__cnic_no']
    inlines = [UserInLine]
    actions = ['view_reports', 'activate_account', 'deactivate_account']

    def full_name(self, obj):
        name = obj.userprofile.full_name()
        return '-' if name == " " else name

    def city(self, obj):
        city = obj.userprofile.city
        return city if city else '-'

    def country(self, obj):
        country = obj.userprofile.country
        return country if country else '-'

    def role(self, obj):
        return 'Admin' if obj.is_staff else obj.userprofile.role

    def is_paired(self, obj):
        return obj.userprofile.is_paired()
    is_paired.boolean = True
    is_paired.short_description = 'Paired'

    def is_activated(self, obj):
        return obj.is_active
    is_activated.boolean = True
    is_activated.short_description = 'Account Active'

    def view_reports(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request,
                                    'Can not view reports for more than one user.',
                                    level = messages.ERROR)
            return
        return HttpResponseRedirect(reverse('accounts:view_reports',
                                            kwargs={'pk' : queryset.first().userprofile.id}))

    def activate_account(modeladmin, request, queryset):
        queryset.update(is_active = True)
        modeladmin.message_user(request, 'Accounts have been activated.')

    def deactivate_account(modeladmin, request, queryset):
        queryset.update(is_active = False)
        modeladmin.message_user(request, 'Accounts have been de-activated.')

admin.site.register(models.Category)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

admin.site.site_header = 'Social Financer Admin'
admin.site.index_title = 'Admin'
admin.site.site_title = 'Social Financer'

