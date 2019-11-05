""" Forms to be used in this app """

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Product, OrderItems

class CustomUserCreationForm(UserCreationForm):
    """ To add fields in built in signup form. """

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address', 'role')


class CustomUserChangeForm(UserChangeForm):
    """ Add fields in user edit form. """

    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'address', 'role')

class SearchForm(forms.Form):
    """ Search by category form. """

    category = forms.CharField(max_length=100)

class ProductsAction(forms.Form):
    """ To apply actions on products. """
    model = Product

class AddProduct(forms.Form):
    """ Form for add products page """

    model = Product

class Order:
    """ Form for order products. """
    model = OrderItems

class ProductForm(forms.Form):
    """ Add products form. """

    class Meta:
        model = Product
        fields = '__all__'
