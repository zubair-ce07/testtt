from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from address.models import Address, Country, Locality, State
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import UserProfile, Profile

admin.site.unregister(User)
admin.site.unregister(Address)
admin.site.unregister(Country)
admin.site.unregister(Locality)
admin.site.unregister(State)


# class UserCreateForm(UserCreationForm):
#     first_name = forms.CharField(label="First name")
#     last_name = forms.CharField(label="Last name")

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name',)

#     def save(self, commit=True):
#         user = super(UserCreateForm, self).save(commit=False)
#         # user.first_name = first_name
#         # user.last_name = last_name
#         if commit:
#             user.save()
#         return user


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    # verbose_name_plural = 'Profile'
    # fk_name = 'user'


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    # def get_inline_instances(self, request, obj=None):
    #     # if not obj:
    #     #     return list()
    #     return super(UserAdmin, self).get_inline_instances(request, obj)

    # def get_formsets(self, request, obj=None):
    #     if not obj:
    #         return []
    #     return super(UserAdmin, self).get_formsets(request, obj)
    # add_form = UserCreateForm
    # # prepopulated_fields = {''}
    # add_fieldsets = ((None, {'fields': (
    #     'first_name', 'last_name', 'username', 'password1', 'password2')}),)
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', ),
    #     }),
    # )
    # fields = ['username', 'password', 'first_name', 'last_name']
    # inlines = [UserProfileInline]


@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    pass

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    pass