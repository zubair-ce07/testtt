from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=20, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}))
        self.fields['last_name'] = forms.CharField(max_length=20, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
        gender_choices = (
            ('Male', u"Male"),
            ('Female', u"Female"),
        )
        self.fields['gender'] = forms.ChoiceField(choices=gender_choices)
        self.fields['date_of_birth'] = forms.DateField(widget=forms.TextInput(
            attrs={'class': 'datepicker'}))

    def save(self, commit=True):
        if commit:
            kwargs = {
                'username': self.cleaned_data['username'],
                'first_name': self.cleaned_data['first_name'],
                'last_name': self.cleaned_data['last_name'],
                'password': self.cleaned_data['password1'],
                'date_of_birth': self.cleaned_data['date_of_birth'],
                'gender': self.cleaned_data['gender']}

            UserProfile.objects.save_user(kwargs)

        return self


class StatusForm(forms.Form):
    status = forms.CharField(max_length=200, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Share yor thoughts'}))
