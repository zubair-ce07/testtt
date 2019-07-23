from django import forms


class AvailableForm(forms.Form):
    Checkin = forms.DateField(widget=forms.SelectDateWidget())
    Checkout = forms.DateField(widget=forms.SelectDateWidget())
