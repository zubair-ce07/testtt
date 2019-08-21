from django import forms

from .models import User


class UserCreationForm(forms.ModelForm):
    password_ = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'date_of_birth', 'gender', 'first_name', 'last_name')

