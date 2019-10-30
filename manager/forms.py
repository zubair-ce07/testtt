from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Product

class ProductsAction(forms.Form):
    """ Class to add checkbox for multiple action perform """
    choices = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple)
