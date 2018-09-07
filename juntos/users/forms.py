from django.contrib.auth.models import User
from django import forms
from validate_email import validate_email


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not validate_email(email):
            raise forms.ValidationError('Enter a valid email')

        if User.objects.filter(email=email):
            raise forms.ValidationError(u'Email already exists')

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()

        if not first_name:
            raise forms.ValidationError("First name is required.")

        return self.cleaned_data["first_name"].strip()

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].strip()

        if not last_name:
            raise forms.ValidationError("Last name is required.")

        return last_name
