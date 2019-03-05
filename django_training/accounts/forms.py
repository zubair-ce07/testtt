from django.contrib.auth.models import User
from django import forms


class SignupForm(forms.ModelForm):
    username = forms.CharField(max_length=255,)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
