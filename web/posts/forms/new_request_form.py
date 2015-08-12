from django import forms
from django.core.exceptions import ValidationError


class NewRequestForm(forms.Form):

    message = forms.CharField(widget=forms.Textarea(), max_length=512, required=False)
    requested_price = forms.DecimalField(max_digits=100, decimal_places=3)

    def clean_requested_price(self):
        requested_price = self.cleaned_data.get('requested_price')
        if requested_price <= 0.0:
            raise ValidationError('Price must be non-negative!')
        return requested_price