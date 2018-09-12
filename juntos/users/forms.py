from django.contrib.auth.models import User, Group
from django import forms
from validate_email import validate_email

from .models import Profile


class UserForm(forms.ModelForm):
    """
    User form
    """
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            # We get the `initial` keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            if kwargs['instance'].groups.all():
                initial['role'] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] = None

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        role = self.cleaned_data.pop('role')
        user = super().save()
        user.groups.set([role])
        user.save()
        return user

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
    """
    Profile form
    """
    class Meta:
        model = Profile
        fields = ('address', 'age', 'profile_photo', 'gender')
