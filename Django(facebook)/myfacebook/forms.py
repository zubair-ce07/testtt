from django import forms
from django.contrib.auth.models import User


class SigninForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class StatusForm(forms.Form):
    status = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Share yor thoughts'}))


class SignupForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def save(self, commit=True):
        if commit:
            username = self.cleaned_data['username']
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            password = self.cleaned_data['password']
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name)
            user.set_password(password)
            user.save()
        return self
