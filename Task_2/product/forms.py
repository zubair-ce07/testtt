from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from djmoney.forms import MoneyWidget

from product.models import Product, ImageURL, ColorURL, SKU


class CreateProductForm(forms.ModelForm):
    # @property
    # def helper(self):
    #     helper = FormHelper()
    #     helper.form_tag = False
    #     helper.layout = Layout(Fieldset('Add Image URL', 'name'), )
    #     return helper

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
            'brand': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Brand'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control form-group', 'placeholder': 'Product Description'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Product Name'}),
            'retailer_sku': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Retailer ID'}),
            'fabric': forms.TextInput(
                attrs={'class': 'form-control form-group', 'placeholder': 'Cloth Fabric Material'})
        }


# class ImageFormHelper(FormHelper):
#     def __init__(self, *args, **kwargs):
#         super(ImageFormHelper, self).__init__(*args, **kwargs)
#         self.form_tag = False
#         self.layout = Layout(Fieldset('Add Image Url', 'url'))
#

class SKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = '__all__'
        widgets = \
            {'id': forms.HiddenInput(), 'out_of_stock': forms.CheckboxInput(attrs={}),
             'color': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Color (Optional)'}),
             'price': MoneyWidget(attrs={'class': 'form-control form-group', 'placeholder': 'Enter SKU price'}),
             'size': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Enter SKU size'})}


class ColorURLForm(forms.ModelForm):
    class Meta:
        model = ColorURL
        fields = ('url',)
        labels = {'url': 'Product Color Page URL'},
        widgets = {'url': forms.URLInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'URL for Product Colors (Optional)'})}


class ImageURLForm(forms.ModelForm):
    class Meta:
        model = ImageURL
        fields = ('url',)
        labels = {'url': 'Product Image URL'}
        widgets = {'url': forms.URLInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'URL for Product Image (Optional)'})}


ImageFormSet = inlineformset_factory(Product, ImageURL, extra=5, can_delete=False, form=ImageURLForm)
ColorFormSet = inlineformset_factory(Product, ColorURL, extra=4, can_delete=False, form=ColorURLForm)
skuFormSet = inlineformset_factory(Product, SKU, extra=5, can_delete=False, form=SKUForm)


class EditProductForm(forms.ModelForm):
    pass
