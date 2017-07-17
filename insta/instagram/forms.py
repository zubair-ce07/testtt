from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)


class EdiProfileForm(UserChangeForm):
    avatar = forms.ImageField(required=False)


class NewPostForm(forms.Form):
    image = forms.ImageField(required=True)
    text = forms.CharField(widget=forms.Textarea)


class SignUpForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2', 'avatar', 'bio',)


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')
