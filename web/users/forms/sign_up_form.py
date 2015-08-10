import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget
from web.users.exceptions import MustContainSpecialCharacter, EmailAlreadyExists, PasswordTooShort
from cities_light.models import City
from cities_light.models import Country
from cities_light.models import Region



class SignUpForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

    first_name = forms.CharField(widget=forms.TextInput(), max_length=100)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=100)

    country = LazyTypedChoiceField(choices=countries, widget=CountrySelectWidget())
    city = forms.ModelChoiceField(queryset=City.objects.all().values_list('name_ascii')[:10])
    street_or_block = forms.CharField(widget=forms.TextInput(), max_length=100)
    zip_code = forms.CharField(widget=forms.TextInput(), max_length=100)

    #forms.ChoiceField(choices=list(countries), widget=CountrySelectWidget())
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    date_of_birth = forms.DateField(initial=datetime.date.today, widget=forms.DateInput(attrs={'type': 'date'}))

    class EmailAlreadyExists(EmailAlreadyExists):
        pass

    class MustContainSpecialCharacter(MustContainSpecialCharacter):
        pass

    class PasswordTooShort(PasswordTooShort):
        pass

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            self.check_if_exists(email=email)
        except self.EmailAlreadyExists as ex:
            raise ValidationError(ex.message)

        return email

    def clean_password(self):

        password = self.cleaned_data.get('password')
        try:
            self.check_password(password=password)
        except (self.PasswordTooShort, self.MustContainSpecialCharacter) as ex:
            raise ValidationError(ex.message)
        return password

    def check_if_exists(self, email):
        if get_user_model().objects.filter(email=email).exists():
            raise self.EmailAlreadyExists

    def check_password(self, password):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise self.PasswordTooShort
        elif not re.search(r'[\W]+', password):
            raise self.MustContainSpecialCharacter
