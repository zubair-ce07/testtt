from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control', 'label': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'label': 'Password'}))

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        return cleaned_data
