from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phone_field import PhoneField

from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField()
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField()
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    address = forms.CharField(max_length=500, required=True)
    city = forms.CharField(max_length=200, required=True)
    state = forms.CharField(max_length=200, required=True)
    zip = forms.CharField(max_length=50, required=True)
    contact = PhoneField()

    class Meta:
        model = Profile
        fields = ['address', 'city', 'state', 'zip', 'contact']
