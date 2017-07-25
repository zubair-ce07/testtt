from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from djmoney.forms import MoneyWidget

from product.models import Product, ImageURL, ColorURL, SKU


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'url': 'Product Page',
            'retailer_sku': 'Product ID',
            'name': 'Product Name',
        }
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control form-group', 'placeholder': 'Product Page URL'}),
            'brand': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Brand (Optional)'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control form-group', 'placeholder': 'Product Description (Optional)'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Product Name'}),
            'retailer_sku': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Retailer ID'}),
            'fabric': forms.TextInput(
                attrs={'class': 'form-control form-group', 'placeholder': 'Cloth Fabric Material (Optional)'})
        }


class EditProductForm(CreateProductForm):
    class Meta:
        model = Product
        exclude = ('retailer_sku',)
        widgets = CreateProductForm.Meta.widgets


class ImageURLForm(forms.ModelForm):
    class Meta:
        model = ImageURL
        fields = ('url',)
        labels = {'url': 'Product Image URL'}
        widgets = {'url': forms.URLInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'URL for Product Image (Optional)'})}


class ColorURLForm(forms.ModelForm):
    class Meta:
        model = ColorURL
        fields = ('url',)
        labels = {'url': 'Product Color Page URL'},
        widgets = {'url': forms.URLInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'URL for Product Colors (Optional)'})}


class SKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = '__all__'
        widgets = \
            {'id': forms.HiddenInput(), 'out_of_stock': forms.CheckboxInput(attrs={}),
             'color': forms.TextInput(
                 attrs={'class': 'form-control form-group', 'placeholder': 'Color (Optional)'}),
             'price': MoneyWidget(attrs={'class': 'form-control form-group', 'placeholder': 'Enter SKU price'}),
             'size': forms.TextInput(
                 attrs={'class': 'form-control form-group', 'placeholder': 'Enter SKU size'})}


ImageFormSet = inlineformset_factory(Product, ImageURL, extra=5, can_delete=False, form=ImageURLForm)
ColorFormSet = inlineformset_factory(Product, ColorURL, extra=4, can_delete=False, form=ColorURLForm)
skuFormSet = inlineformset_factory(Product, SKU, extra=5, can_delete=False, form=SKUForm)
