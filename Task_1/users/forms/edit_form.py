from django import forms
from django.contrib.auth.models import User
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField

from task1.dict import dict
from users.forms.signup_form import phone_validator

attr = dict({'class': 'form-control form-group'})


class EditForm(forms.ModelForm):
    country = LazyTypedChoiceField(choices=countries, widget=forms.Select(attrs=attr), required=False)
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs=attr))
    phone_number = forms.CharField(validators=[phone_validator], required=False, widget=forms.TextInput(
        attrs=attr.update({'placeholder': 'Format: +123456789 (Optional)'})))
    address = forms.CharField(max_length=1000, required=False,
                              widget=forms.Textarea(attrs=attr.update({'placeholder': 'Address (Optional)'})))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'country', 'image', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs=attr.update({'placeholder': 'e.g. John (Optional)'})),
            'last_name': forms.TextInput(attrs=attr.update({'placeholder': 'e.g. Doe (Optional)'})),
            'email': forms.TextInput(attrs=attr.update({'placeholder': 'Email address'})),
        }

    def __init__(self, *args, **kwargs):
        self.FILES = kwargs.pop('FILES', None)
        super(EditForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user_profile = self.instance.userprofile
        user_profile.phone_number = self.cleaned_data.get('phone_number')
        user_profile.address = self.cleaned_data.get('address')
        user_profile.country = self.cleaned_data.get('country')
        if self.FILES.get('image'):
            user_profile.image = self.FILES.get('image')
        elif not self.cleaned_data.get('image'):
            user_profile.image = None
        user_profile.save()
        return super(EditForm, self).save(commit=commit)
