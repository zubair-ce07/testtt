from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    email = forms.CharField(max_length=250, required=True, widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
