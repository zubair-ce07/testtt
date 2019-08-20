"""user Profile Forms Module.

This module has diffrent forms for the user profile app.
"""
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    """User Registration form.

    This is user regitration from for our customized user model, it inherit
    the UserCreationForm and override it's Fields and model.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'first_name', 'last_name', 'gender', 'phone_no', 'address']


class UserUpdateForm(forms.ModelForm):
    """User Update form.

    This is user Update from for our customized user model, it inherit
    the ModelForm and override it's Fields and model.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'gender', 'phone_no', 'address']


class UserLoginForm(AuthenticationForm):
    """User Login form.

    This is user login from for our customized user model, it inherit
    the AuthticateForm and override it's Fields and model and username
    fields since we are using email for login.
    """
    username = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']
