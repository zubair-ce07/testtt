from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django.core.validators import RegexValidator
from django.db.models.fields.files import FileField, ImageFieldFile, ImageField


class UserCreateForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username', widget=forms.TextInput(
        attrs={'class': 'form-group form-control',
               'placeholder': '150 characters or fewer. Letters, digits and @/./+/-/_ only.'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-group', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-group', 'placeholder': 'Confirm Password'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-group form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(
        attrs={'class': 'form-group form-control', 'placeholder': 'e.g. John (Optional)'}, ))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-group', 'placeholder': 'e.g. Doe (Optional)', }, ))
    phone_number = forms.CharField(validators=[
        RegexValidator(regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'.")],
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'Format: +123456789 (Optional)'}))
    country = LazyTypedChoiceField(choices=countries, widget=forms.Select(attrs={'class': 'form-control form-group'}),
                                   required=False)
    address = forms.CharField(max_length=1000, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-group', 'placeholder': 'Address (Optional)'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control form-group'}))

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        username = cleaned_data['username']
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        UnicodeUsernameValidator().__call__(username)
        if User.objects.filter(username=username):
            raise forms.ValidationError('A user with that username already exists.')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords do not match.')
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control form-group', 'label': 'Username', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-group', 'label': 'Password', 'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        return cleaned_data
