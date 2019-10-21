"""Module for User profile form and update form."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserProfileForm(UserCreationForm):
    """Class for Initializing user profile."""

    class Meta:
        """Meta class"""
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password1', 'password2', 'phone_number', 'location', 'age')


class UpdateForm(forms.ModelForm):
    """Class for Initializing user update profile."""

    class Meta:
        """Meta class"""
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name',
                  'phone_number', 'location', 'age')
