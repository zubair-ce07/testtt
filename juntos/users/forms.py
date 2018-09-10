from django.contrib.auth.models import User
from django import forms
from validate_email import validate_email

from users.models import Profile


class UserForm(forms.ModelForm):
    """
    User form
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        """
        Validate email
        :return: Email or ValidationError
        """
        email = self.cleaned_data.get('email')

        if not validate_email(email):
            raise forms.ValidationError('Enter a valid email')

        already_exists = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if already_exists:
            raise forms.ValidationError('Email already exists')

        return email

    def clean_first_name(self):
        """
        Validate first name
        :return: first name or ValidationError
        """
        first_name = self.cleaned_data["first_name"].strip()

        if not first_name:
            raise forms.ValidationError("First name is required.")

        return first_name

    def clean_last_name(self):
        """
        Validate last name
        :return: last name or ValidationError
        """
        last_name = self.cleaned_data["last_name"].strip()

        if not last_name:
            raise forms.ValidationError("Last name is required.")

        return last_name


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'age', 'profile_photo', 'gender')
