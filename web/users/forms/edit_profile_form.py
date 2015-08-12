import datetime
from cities_light.models import City
from django import forms
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget


class EditProfileForm(forms.Form):

    first_name = forms.CharField(widget=forms.TextInput(), max_length=100)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=100)

    country = LazyTypedChoiceField(choices=countries, widget=CountrySelectWidget())
    city = forms.ModelChoiceField(queryset=City.objects.all())
    street_or_block = forms.CharField(widget=forms.TextInput(), max_length=100)
    zip_code = forms.CharField(widget=forms.TextInput(), max_length=100)

    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    date_of_birth = forms.DateField(initial=datetime.date.today, widget=forms.DateInput(attrs={'type': 'date'}))