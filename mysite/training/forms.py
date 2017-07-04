from django import forms
from django.contrib.auth.models import User

from .models import Trainer, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    picture = forms.ImageField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['picture']
