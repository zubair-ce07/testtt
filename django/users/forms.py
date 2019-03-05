from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


ROLES = [
    ('buyer', 'Buyer'),
    ('seller', 'Seller')
]


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


class UpdateUserForm(UserForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):

    role = forms.ChoiceField(choices=ROLES, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields = ('role',)
