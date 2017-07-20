from django import forms
from django.contrib.auth.forms import UserCreationForm

from twitter.models import User


class UserSignUpForm(UserCreationForm):
#    username = forms.CharField(max_length=User._meta.get_field('username').max_length)

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data['username']).exists():
            raise forms.ValidationError("username already exist")
        return self.cleaned_data['username']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class AdminUserSignUpForm(UserSignUpForm):
    class Meta(UserSignUpForm.Meta):
        fields = ['is_active', 'is_staff', 'is_superuser',  'followers']


class TweetForm(forms.Form):
    tweet_text = forms.CharField(widget=forms.Textarea)


class FollowForm(forms.Form):
    follower_username=forms.CharField(widget=forms.HiddenInput())