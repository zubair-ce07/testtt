from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Product

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address', 'type')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'address', 'type')

class SearchForm(forms.Form):
    category = forms.CharField(max_length=100)

class ProductsAction(forms.Form):
    model = Product
