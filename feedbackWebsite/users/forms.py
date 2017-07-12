from django import forms
from django.contrib.auth.models import User


class UserRegisterForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=254)
    last_name = forms.CharField(max_length=254)
    password = forms.CharField(required=False, widget=forms.PasswordInput, initial='')


class PersonProfileForm(forms.Form):
    mobile_number = forms.CharField(max_length=30, required=False)
    current_address = forms.CharField(max_length=254, required=False)
    permanent_address = forms.CharField(max_length=254, required=False)
