"""
this module contains the forms used in this
"""
from django.contrib.auth.models import User
from django import forms

# from django.contrib.auth.forms import UserChangeForm


# class UserEditForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email']
#         exclude = ['password']

class UserEditForm(forms.ModelForm):
    """
    this is a user defined edit form, the built-in form have some problems so i used it
    """

    class Meta:
        """
        Meta class of UserEditForm
        """
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
