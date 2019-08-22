from django import forms

from .models import Saloon


class ShopUpdateForm(forms.ModelForm):
    class Meta:
        model = Saloon
        fields = ['shop_name', 'phone_no']
