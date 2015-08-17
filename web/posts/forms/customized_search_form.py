from django import forms


class CustomizedSearchForm(forms.Form):
    KIND_CHOICES = [('house', 'House'), ('plot', 'Plot'),
                    ('commercial_plot', 'Commercial Plot'), ('commercial_building', 'Commercial Building'),
                    ('flat', 'Flat'), ('shop', 'Shop'), ('farm_house', 'Farm House'), ]

    country = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden', 'id': 'country', 'placeholder': 'Country', 'disabled': 'true'}), required=False,
        max_length=100)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden', 'id': 'administrative_area_level_1', 'placeholder': 'State', 'disabled': 'true'}),
        required=False,
        max_length=100)
    city = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden', 'id': 'locality', 'placeholder': 'City', 'disabled': 'true'}), required=False,
        max_length=100)
    route = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden', 'id': 'route', 'placeholder': 'Route', 'disabled': 'true'}), required=False,
        max_length=100)

    kind = forms.ChoiceField(widget=forms.Select(attrs={'class': ' form-control'}), choices=KIND_CHOICES)

    max_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price($)'}),
                                   required=False, max_digits=100, decimal_places=3)
