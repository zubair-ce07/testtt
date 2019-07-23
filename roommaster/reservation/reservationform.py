from django import forms


class ReservationForm(forms.Form):
    Rent = forms.DecimalField()
    Customer = forms.ChoiceField()
