from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

USER_TYPES = [(1, "CEO"), (2, "Manager"), (3, "Worker"), ]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'address')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('username', 'password')


class CompetencyForm(forms.Form):
    comment = forms.CharField(max_length=500, required=False)
    team_work = forms.IntegerField(min_value=1, max_value=10, required=True)
    leadership = forms.IntegerField(min_value=1, max_value=10, required=True)

    class Meta:
        fields = ('comment', 'team_work', 'leadership')


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'address')
