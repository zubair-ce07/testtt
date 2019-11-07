""" Forms to be used in users app """

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """ To add fields in built in signup form. """

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address', 'role')


class CustomUserChangeForm(UserChangeForm):
    """ Add fields in user edit form. """

    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'address', 'role')