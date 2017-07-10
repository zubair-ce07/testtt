from django.contrib import admin
from django.contrib.auth.models import User
from address.models import Address, Country, Locality, State

from .models import UserProfile

admin.site.unregister(User)
admin.site.unregister(Address)
admin.site.unregister(Country)
admin.site.unregister(Locality)
admin.site.unregister(State)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    fields = ['username', 'password', 'first_name', 'last_name']
    inlines = [UserProfileInline]


@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    pass
