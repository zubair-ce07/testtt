from django import forms
from reservation.models import Customer
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AvailabilityForm(forms.Form):
    checkin = forms.DateField(widget=forms.SelectDateWidget())
    checkout = forms.DateField(widget=forms.SelectDateWidget())


class ReservationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.room = kwargs.get('room')
        self.checkin = kwargs.get('checkin')
        self.checkout = kwargs.get('checkout')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['room'].widget = forms.TextInput(attrs={'value': self.room, 'readonly': 'readonly'})
        self.fields['checkin'].widget = forms.TextInput(attrs={'value': self.checkin, 'readonly': 'readonly'})
        self.fields['checkout'].widget = forms.TextInput(attrs={'value': self.checkout, 'readonly': 'readonly'})

    room = forms.CharField()
    rent = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Rent'}), min_value=1)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    checkin = forms.DateField()
    checkout = forms.DateField()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
