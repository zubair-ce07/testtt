from django import forms
from django.contrib.auth.models import User

from registration.models import UserProfile


class EditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                            'placeholder': 'Email'}),
        }
