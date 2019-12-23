from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder ': 'Username', 'labelClass': 'zmdi-account material-icons-name '}))

    password = forms.CharField(max_length=35, widget=forms.PasswordInput(
        attrs={'placeholder ': 'Password', 'labelClass': 'zmdi-lock'}))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(
        attrs={'placeholder ': 'First Name', 'labelClass': 'zmdi-account material-icons-name '}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(
        attrs={'placeholder ': 'Last Name', 'labelClass': 'zmdi-account material-icons-name '}))

    username = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(
        attrs={'placeholder ': 'Username', 'labelClass': 'zmdi-account material-icons-name '}))

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
                                 attrs={'placeholder ': 'Email', 'labelClass': 'zmdi-email '}))

    password1 = forms.CharField(max_length=35, widget=forms.PasswordInput(
                                    attrs={'placeholder ': 'Password', 'labelClass': 'zmdi-lock '}))
    password2 = forms.CharField(max_length=35,widget=forms.PasswordInput(
                                    attrs={'placeholder ': 'Re Enter Password', 'labelClass': 'zmdi-lock '}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)
