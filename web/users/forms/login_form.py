from django import forms


class LogInForm(forms.Form):

    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                            max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               max_length=100)