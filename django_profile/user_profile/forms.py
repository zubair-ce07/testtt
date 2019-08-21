"""user Profile Forms Module.

This module has diffrent forms for the user profile app.
"""
from django import forms
from django.contrib.auth import password_validation, authenticate
from django.utils.translation import gettext_lazy as _

from .models import MyUser


class UserRegisterForm(forms.ModelForm):
    """User Registration From.

    A form that creates a user, with no privileges, from the given email and
    password.
    """

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        """Meta for User Registration Form
        """
        model = MyUser
        fields = ("email", 'password1', 'password2',
                  'first_name', 'last_name', 'gender', 'address', 'phone_no')

    def clean_password2(self):
        """Match Password.

        This method match password and confrim password and and return true if both are same
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """User Update form.

    This is user Update from for our customized user model, it inherit
    the ModelForm and override it's Fields and model.
    """
    class Meta:
        """Meta for User User Update Form
        """
        model = MyUser
        fields = ['email', 'first_name',
                  'last_name', 'gender', 'phone_no', 'address']


class UserLoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct Email and password. Note that both "
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
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password)
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
