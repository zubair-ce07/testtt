from django.contrib.auth.models import Group
from django.contrib import admin
from twitter.models import User, Tweet
from twitter.forms import AdminUserSignUpForm


class UserAdmin(admin.ModelAdmin):
    form = AdminUserSignUpForm
    list_display = ('username','first_name', 'email')
    search_fields = ('username', 'first_name', 'last_name')
    filter_horizontal = ('followers',)


admin.site.register(User, UserAdmin)
admin.site.register(Tweet)

admin.site.unregister(Group)
