from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))

    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))

    class Meta:
        model = UserProfile
        fields = UserCreationForm.Meta.fields + (
            'password1', 'password2', 'first_name', 'last_name', 'gender',
            'date_of_birth'
        )
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'class': 'datepicker'})
        }

    def save(self, commit=True):
        return UserProfile.objects.create_user(**self.cleaned_data)


class StatusForm(forms.Form):
    status = forms.CharField(max_length=200, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Share yor thoughts'}))
