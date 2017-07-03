from django.forms import ModelForm
from django import forms
from main.models import Tweet
from django.contrib.auth.models import User
from django.contrib.admin import widgets

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
    pub_date = forms.DateTimeField(widget=forms.SelectDateWidget)
