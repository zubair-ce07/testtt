from django import forms


class LogInForm(forms.Form):

    email = forms.CharField(widget=forms.TextInput(), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)