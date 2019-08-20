"""user Profile Forms Module.

This module has diffrent forms for the user profile app.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
import unicodedata

from .models import MyUser


class UserRegisterForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
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
        model = MyUser
        fields = ("email", 'password1', 'password2',
                  'first_name', 'last_name', 'gender', 'address', 'phone_no')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({
                                                                             'autofocus': True})

    def clean_password2(self):
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
        model = MyUser
        fields = ['email', 'first_name',
                  'last_name', 'gender', 'phone_no', 'address']


class UserLoginForm(AuthenticationForm):
    """User Login form.

    This is user login from for our customized user model, it inherit
    the AuthticateForm and override it's Fields and model and username
    fields since we are using email for login.
    """
    username = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ['email', 'password']
