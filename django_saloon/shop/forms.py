"""shop forms module."""
from django import forms

from .models import Saloon


class ShopUpdateForm(forms.ModelForm):
    """shop update form."""
    class Meta:
        model = Saloon
        fields = ['shop_name', 'phone_no', 'address']

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ShopUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['phone_no'].required = True
        self.fields['shop_name'].required = True
        self.fields['address'].required = True
