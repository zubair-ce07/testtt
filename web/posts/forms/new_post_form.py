from cities_light.models import City
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget


class NewPostForm(forms.Form):

    KIND_CHOICES = [('house', 'House'), ('plot', 'Plot'),
                    ('commercial_plot', 'Commercial Plot'), ('commercial_building', 'Commercial Building'),
                    ('flat', 'Flat'), ('shop', 'Shop'), ('farm_house', 'Farm House'),]

    title = forms.CharField(widget=forms.TextInput(), max_length=255)
    area = forms.DecimalField(max_digits=100, decimal_places=3)

    country = LazyTypedChoiceField(choices=countries, widget=CountrySelectWidget())
    city = forms.ModelChoiceField(queryset=City.objects.all())
    street_or_block = forms.CharField(widget=forms.TextInput(), max_length=100)
    zip_code = forms.CharField(widget=forms.TextInput(), max_length=100)

    description = forms.CharField(widget=forms.Textarea(), max_length=1024)
    kind = forms.ChoiceField(choices=KIND_CHOICES)
    contact_number = forms.CharField(widget=forms.TextInput(), max_length=50)
    demand = forms.DecimalField(max_digits=100, decimal_places=3)
    expired_on = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError('Title is too short elaborate more!')
        return title

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area <= 0.0:
            raise ValidationError('Area must be non-negative!')
        return area

    def clean_expired_on(self):
        expired_on = self.cleaned_data.get('expired_on')
        time_delta = expired_on - timezone.now()
        if time_delta.total_seconds() < 0:
            raise ValidationError('give valid expiry time for your post')
        return expired_on

    def clean_demand(self):
        demand = self.cleaned_data.get('demand')
        if demand <= 0.0:
            raise ValidationError('Demanded price must be non-negative!')
        return demand