from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class UserSignUpForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'username']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class TweetForm(forms.Form):
    tweet_text = forms.CharField(widget=forms.Textarea)
