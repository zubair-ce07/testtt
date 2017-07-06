from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean_username(self):
    #     data = self.cleaned_data['username']
    #     if len(data) > 1:
    #         raise ValidationError('Max length')
    #     return data
