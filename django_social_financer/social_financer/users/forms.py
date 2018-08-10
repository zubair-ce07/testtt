from django.forms import ModelForm
from .models import UserProfile

class SignUpForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'cnic_no', 'address', 'country', 'city',
                  'postal_code', 'email', 'password', 'phone_no', 'role', 'categories']