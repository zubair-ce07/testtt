import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from taskmanager.models import Task
from taskmanager.validators import validate_username_unique, validate_email_unique

from taskmanager.validators import validate_user_profile_picture

from taskmanager.models import CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    due_date = forms.DateField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "type": 'date',
            "min": datetime.date.today(),
            "value": datetime.date.today() + datetime.timedelta(days=7)
        })
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'username', 'email', 'first_name', 'last_name', 'birthday', 'address',
                  'password1', 'password2']

    # field_order = ['profile_picture', 'username', 'email', 'first_name', 'last_name', 'birthday', 'address',
    #                'password1', 'password2']

    username = forms.CharField(
        max_length=50,
        label='Username:',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username"
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
    first_name = forms.CharField(
        max_length=50,
        label="First Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name"
        })
    )

    last_name = forms.CharField(
        max_length=50,
        label="Last Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last Name"
        })
    )

    address = forms.Textarea()

    birthday = forms.DateField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "type": 'date',
            "max": datetime.date.today(),
            "value": datetime.date.today()
        })
    )

    profile_picture = forms.ImageField(
        validators=[validate_user_profile_picture]
    )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.profile_picture = self.cleaned_data["profile_picture"]
        user.address = self.cleaned_data["address"]
        user.birthday = self.cleaned_data["birthday"]
        if commit:
            user.save()
        return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'username', 'email', 'first_name', 'last_name', 'birthday', 'address', ]

    username = forms.CharField(
        max_length=50,
        label='Username:',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username"
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
