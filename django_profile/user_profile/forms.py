from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'first_name', 'last_name', 'gender', 'phone_no', 'address']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'gender', 'phone_no', 'address']


class UserLoginForm(AuthenticationForm):

    username = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']
