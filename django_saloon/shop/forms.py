"""Shop forms module."""
from django import forms

from shop.models import Saloon
from core.constants import SHOP_NAME, PHONE_NO, ADDRESS


class ShopUpdateForm(forms.ModelForm):
    """Shop update form."""

    class Meta:
        """shop update form meta."""

        model = Saloon
        fields = ['shop_name', 'phone_no', 'address']

    def __init__(self, *args, **kwargs):
        """Shop Update update form init."""
        # first call parent's constructor
        super(ShopUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields[PHONE_NO].required = True
        self.fields[SHOP_NAME].required = True
        self.fields[ADDRESS].required = True
