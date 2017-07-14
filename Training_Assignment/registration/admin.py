from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from address.models import Address, Country, Locality, State
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import UserProfile

admin.site.unregister(User)
admin.site.unregister(Country)
admin.site.unregister(Locality)
admin.site.unregister(State)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    exclude = ('user', )
