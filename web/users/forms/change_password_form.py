import re

from django import forms

from web.users.exceptions import PasswordTooShort, MustContainSpecialCharacter


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old password'}), max_length=100)
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}), max_length=100)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), max_length=100)

    class MustContainSpecialCharacter(MustContainSpecialCharacter):
        pass

    class PasswordTooShort(PasswordTooShort):
        pass

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.check_password(self.cleaned_data.get('old_password')):
            password = self.cleaned_data.get('new_password')
            confirm_password = self.cleaned_data.get('confirm_password')

            if password and confirm_password != password:
                raise forms.ValidationError("Passwords don't match")
        else:
            raise forms.ValidationError("Please enter the correct old password")

        return self.cleaned_data

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        try:
            self.validate_password(password=password)
        except (self.PasswordTooShort, self.MustContainSpecialCharacter) as ex:
            raise forms.ValidationError(ex.message)
        return password

    def validate_password(self, password):
        password = self.cleaned_data.get('new_password')
        if len(password) < 8:
            raise self.PasswordTooShort
        elif not re.search(r'[\W]+', password):
            raise self.MustContainSpecialCharacter