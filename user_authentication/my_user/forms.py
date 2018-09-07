from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm


# class UserEditForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email']
#         exclude = ['password']

class UserEditForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
