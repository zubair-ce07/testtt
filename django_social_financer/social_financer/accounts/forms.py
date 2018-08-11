from django.forms import ModelForm
from django import forms
from .models import UserProfile

class SignUpForm(ModelForm):
    first_name = forms.CharField(max_length=30, min_length=1, label="First Name")
    last_name = forms.CharField(max_length=30, min_length=1, label="Last Name")
    email_address = forms.EmailField(min_length=7, label="Email address")
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=16, label="Password")
    class Meta:
        model = UserProfile
        exclude = ['pairId']
        # fields = ['user.first_name', 'user.last_name', 'cnic_no', 'address', 'country', 'city',
        #           'postal_code', 'user.email', 'user.password', 'phone_no', 'role', 'categories']

        fields = ['first_name', 'last_name', 'email_address', 'password','cnic_no', 'address', 'city', 'country',
                  'postal_code', 'phone_no', 'role', 'categories']

