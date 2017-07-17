from django import forms
from django.contrib.auth.models import User


class UserCreateForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username',
                               help_text='150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data['username']
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if User.objects.filter(username=username):
            raise forms.ValidationError('A user with that username already exists.')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords do not match.')
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control', 'label': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'label': 'Password'}))

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        return cleaned_data
