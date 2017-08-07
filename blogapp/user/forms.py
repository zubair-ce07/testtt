from django.forms import CharField, PasswordInput, TextInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = CharField(label="Username", max_length=30,
                         widget=TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(label="Password", max_length=30,
                         widget=PasswordInput(attrs={'placeholder': 'Password'}))


class SignUpForm(UserCreationForm):
    password1 = CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}), required=True)
    password2 = CharField(widget=PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {'username': TextInput(attrs={'placeholder': 'Username'}),
                   'email': TextInput(attrs={'placeholder': 'Email'})}
