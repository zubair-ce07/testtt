from django import forms
from reservation.models import Customer
from django.core.validators import MinValueValidator


class AvailabilityForm(forms.Form):
    checkin = forms.DateField(widget=forms.SelectDateWidget())
    checkout = forms.DateField(widget=forms.SelectDateWidget())


class ReservationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room')
        self.checkin = kwargs.pop('checkin')
        self.checkout = kwargs.pop('checkout')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['room'].widget = forms.TextInput(attrs={'value': self.room, 'readonly': 'readonly'})
        self.fields['checkin'].widget = forms.TextInput(attrs={'value': self.checkin, 'readonly': 'readonly'})
        self.fields['checkout'].widget = forms.TextInput(attrs={'value': self.checkout, 'readonly': 'readonly'})

    room = forms.CharField()
    rent = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Rent'}), min_value=1)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    checkin = forms.DateField()
    checkout = forms.DateField()
