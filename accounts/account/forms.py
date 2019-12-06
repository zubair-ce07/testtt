from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError(
                    "This User does not exist in Database")

            if not user.check_password(password):
                raise forms.ValidationError("Password does not match")

            if not user.is_active:
                raise forms.ValidationError("User is not active")
            
        return super(LoginForm, self).clean(*args, **kwargs)


class EditProfile(UserChangeForm):

    class Meta:
        model = User
        fields = {
            'email',
            'first_name',
            'last_name',
            'password'
        }
