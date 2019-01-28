from django import forms


class LoginForm(forms.Form):
    user_name = forms.CharField(label='User Name', max_length=15)
    password = forms.CharField(widget=forms.PasswordInput())
