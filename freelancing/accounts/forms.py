from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'country', 'profile_image')
