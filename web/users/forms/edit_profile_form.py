import datetime
from cities_light.models import City
from django import forms
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget


class EditProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
                                 max_length=100)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
                                max_length=100)

    country = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'country', 'placeholder': 'Country', 'disabled': 'true'}), max_length=100)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'administrative_area_level_1', 'placeholder': 'State', 'disabled': 'true'}), max_length=100)
    city = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'locality', 'placeholder': 'City', 'disabled': 'true'}), max_length=100)
    route = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'route', 'placeholder': 'Route', 'disabled': 'true'}), max_length=100)
    street_or_block = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'street_number', 'placeholder': 'Street or block', 'disabled': 'true'}), max_length=100)
    zip_code = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'postal_code', 'placeholder': 'Zip code', 'disabled': 'true'}), max_length=100)

    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    date_of_birth = forms.DateField(initial=datetime.date.today,
                                    widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))