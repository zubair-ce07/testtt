from django import forms
from django.forms import ValidationError


class UserSignInForm(forms.Form):
    """ Validates user's signin credentials """
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class UserSignUpForm(forms.Form):
    """ Validates user's signup credentials """
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(required=True)


class UserChangePasswordForm(forms.Form):
    """ Validates user's change password credentials """
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)


class UserEditProfileForm(forms.Form):
    """ Validates user's signin credentials """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    qualification = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)
