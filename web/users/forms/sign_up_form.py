import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
import re
from web.users.exceptions import MustContainSpecialCharacter, EmailAlreadyExists, PasswordTooShort


class SignUpForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               max_length=100)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}), max_length=100)

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
                                 max_length=100)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
                                max_length=100)

    country = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'country', 'placeholder': 'Country', 'disabled': 'true'}), max_length=100)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'administrative_area_level_1', 'placeholder': 'State', 'disabled': 'true'}), max_length=100)
    city = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'locality', 'placeholder': 'City', 'disabled': 'true'}), max_length=100)
    route = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'route', 'placeholder': 'Route', 'disabled': 'true'}), max_length=100)
    street_or_block = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'street_number', 'placeholder': 'Street or block', 'disabled': 'true'}), max_length=100)
    zip_code = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'postal_code', 'placeholder': 'Zip code', 'disabled': 'true'}), max_length=100)

    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    date_of_birth = forms.DateField(initial=datetime.date.today,
                                    widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class EmailAlreadyExists(EmailAlreadyExists):
        pass

    class MustContainSpecialCharacter(MustContainSpecialCharacter):
        pass

    class PasswordTooShort(PasswordTooShort):
        pass

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password != password:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

    def clean_email(self):

        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
            self.check_if_exists(email=email)
        except self.EmailAlreadyExists as ex:
            raise ValidationError(ex.message)
        except ValidationError:
            raise ValidationError('email is not correct')

        return email

    def clean_password(self):

        password = self.cleaned_data.get('password')
        try:
            self.check_password(password=password)
        except (self.PasswordTooShort, self.MustContainSpecialCharacter) as ex:
            raise ValidationError(ex.message)
        return password

    def check_if_exists(self, email):
        if get_user_model().objects.filter(email=email).exists():
            raise self.EmailAlreadyExists

    def check_password(self, password):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise self.PasswordTooShort
        elif not re.search(r'[\W]+', password):
            raise self.MustContainSpecialCharacter
