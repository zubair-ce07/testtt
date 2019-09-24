"""Customer forms module."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer


class UserRegisterForm(UserCreationForm):
    """User creation form."""

    email = forms.EmailField()

    class Meta:
        """User Registration form Meta."""

        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'first_name', 'last_name']


class UserUpdateForm(forms.ModelForm):
    """User update form."""

    email = forms.EmailField()

    class Meta:
        """User Update form Meta."""

        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        """User update init method."""
        # first call parent's constructor
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class CustomerUpdateForm(forms.ModelForm):
    """Customer update form."""

    class Meta:
        """Customer update form meta."""

        model = Customer
        fields = ['phone_no']

    def __init__(self, *args, **kwargs):
        """Update Form init method."""
        # first call parent's constructor
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['phone_no'].required = True
