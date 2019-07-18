import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TaskForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Task title"
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter description!"
            })
    )
    assignee = forms.ModelChoiceField(queryset=User.objects.all())
    due_date = forms.DateField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "type": 'date',
            "min": datetime.date.today(),
            "value": datetime.date.today() + datetime.timedelta(days=7)
        })
    )


class UserRegistrationForm(UserCreationForm):
    field_order = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    username = forms.CharField(
        max_length=50,
        label='Username:',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username"
        })
    )
    first_name = forms.CharField(
        max_length=50,
        label="First Name:",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name"
        })
    )
    last_name = forms.CharField(
        max_length=50,
        label="Last Name:",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last Name"
        })
    )
    email = forms.CharField(
        max_length=50,
        label="Email",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
            "type": "email"
        })
    )

    password1 = forms.CharField(
        label="Password:",
        help_text="150 characters or fewer. Atleast 8 characters, Not too common, Letters, digits and @/./-/+/_ "
                  "allowed. ",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
            'type': "password",
        })
    )

    password2 = forms.CharField(
        label="Confirm Password:",
        help_text="Enter the same password as before.",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password",
            "type": "password"
        })
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        if User.objects.get(email=email):
            self.add_error(field='email', error='This email address already exists')
