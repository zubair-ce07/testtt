"""core forms module."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    """user creation form."""
    email = forms.EmailField()

    class Meta:
        """User Registration form Meta"""
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'first_name', 'last_name']
