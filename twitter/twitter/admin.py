from django.contrib.auth.models import Group
from django.contrib import admin
from twitter.models import User, Tweet
from twitter.forms import UserSignUpForm


class UserAdmin(admin.ModelAdmin):
    form = UserSignUpForm
    list_display = ('is_staff','username', 'email')
    filter_horizontal = ('followers',)


admin.site.register(User, UserAdmin)
admin.site.register(Tweet)

admin.site.unregister(Group)
