from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import FBUserCreationForm, FBUserChangeForm
from .models import FBUser


class CustomUserAdmin(UserAdmin):
    add_form = FBUserCreationForm
    form = FBUserChangeForm
    model = FBUser
    list_display = ['email', 'username',]


admin.site.register(FBUser, CustomUserAdmin)
