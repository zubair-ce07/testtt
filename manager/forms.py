from django import forms
from .models import Product, OrderItems

class ProductsAction(forms.Form):
    """ Class to add checkbox for multiple action perform """
    choices = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), \
        widget=forms.CheckboxSelectMultiple)

class AddProduct(forms.Form):
    """ Form for add products page """

    model = Product

class Order:
    """ Form for order products. """
    model = OrderItems

class ProductForm(forms.ModelForm):
    """ Add products form. """

    class Meta:
        model = Product
        fields = '__all__'
