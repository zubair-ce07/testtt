from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from web.posts.models import Post


class NewPostForm(forms.Form):

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                            max_length=255)
    area = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area (in square meters)'}),
        max_digits=100, decimal_places=3)

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

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write description'}), max_length=1024)
    kind = forms.ChoiceField(widget=forms.Select(attrs={'class':' form-control'}), choices=Post.KindChoices.CHOICES)
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact #'}), max_length=50)
    demand = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price($)'}),
                                max_digits=100, decimal_places=3)

    expired_on = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}))

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