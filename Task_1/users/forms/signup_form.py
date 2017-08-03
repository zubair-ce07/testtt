from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField

from users.forms.dict import dict

attr = dict({'class': 'form-control form-group'})
message = "Phone number must be entered in the format: '+9999999999'."
phone_validator = RegexValidator(regex=r'^\+?\d{10,15}$', message=message)


class SignupForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Diplay Picture',
                             widget=forms.FileInput(attrs=attr))
    country = LazyTypedChoiceField(choices=countries, widget=forms.Select(attrs=attr), required=False)
    password2 = forms.CharField(label='Password (Again)',
                                widget=forms.PasswordInput(attrs=attr.update({'placeholder': 'Confirm Password'})))
    phone_number = forms.CharField(validators=[phone_validator], required=False, widget=forms.TextInput(
        attrs=attr.update({'placeholder': 'Format: +123456789 (Optional)'})))
    address = forms.CharField(max_length=1000, required=False,
                              widget=forms.Textarea(attrs=attr.update({'placeholder': 'Address (Optional)'})))

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data['password']
        password2 = cleaned_data['password2']

        if password and password2 and password != password2:
            raise forms.ValidationError('The passwords do not match.')
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'phone_number', 'country',
                  'image', 'address')
        labels = {'email': 'Email'}
        help_texts = {'username': None}
        widgets = {'username': forms.TextInput(attrs=attr.update({
            'placeholder': '150 characters or fewer. Letters, digits and @/./+/-/_ only.'})),
            'password': forms.PasswordInput(attrs=attr.update({'placeholder': 'Enter Password'})),
            'email': forms.EmailInput(attrs=attr.update({'placeholder': 'Email Address', 'required': True})),
            'last_name': forms.TextInput(attrs=attr.update({'placeholder': 'e.g. Doe (Optional)', 'required': False})),
            'first_name': forms.TextInput(attrs=attr.update({'placeholder': 'e.g. John (Optional)', 'required': False}))
        }
