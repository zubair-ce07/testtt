from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation, authenticate

from .models import Customer, SaloonUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = SaloonUser
        fields = ['username', 'email', 'password1',
                  'password2', 'first_name', 'last_name']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = SaloonUser
        fields = ['username', 'email', 'first_name', 'last_name']


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_no']


class UserLoginForm(forms.Form):

    username = forms.CharField(label=_("Username"))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct username and password. Note that both "
            "fields may be case-sensitive."
        ),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """Find User by email and password.

        This method find user by email and password.
        """
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login')

        return self.cleaned_data

    def get_user(self):
        """Get user.

        This method get user from cache
        """
        return self.user_cache
