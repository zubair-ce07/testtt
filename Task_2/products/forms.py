from django import forms
from djmoney.forms import MoneyWidget

from products.dict import dict
from products.models import Product, ImageURL, ColorURL, Sku

attr = dict({'class': 'form-control form-group'})


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
            'url': forms.URLInput(attrs=attr.update({'placeholder': 'Product Page URL'})),
            'brand': forms.TextInput(attrs=attr.update({'placeholder': 'Brand (Optional)'})),
            'description': forms.TextInput(attrs=attr.update({'placeholder': 'Product Description (Optional)'})),
            'name': forms.TextInput(attrs=attr.update({'placeholder': 'Product Name'})),
            'retailer_sku': forms.TextInput(attrs=attr.update({'placeholder': 'Retailer ID'})),
            'fabric': forms.TextInput(attrs=attr.update({'placeholder': 'Cloth Fabric Material (Optional)'})),
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
        widgets = {'url': forms.URLInput(attrs=attr.update({'placeholder': 'URL for Product Image (Optional)'}))}


class ColorURLForm(forms.ModelForm):
    class Meta:
        model = ColorURL
        fields = ('url',)
        labels = {'url': 'Product Color Page URL'},
        widgets = {'url': forms.URLInput(attrs=attr.update({'placeholder': 'URL for Product Colors (Optional)'}))}


class SkuForm(forms.ModelForm):
    class Meta:
        model = Sku
        fields = '__all__'
        widgets = {'id': forms.HiddenInput(),
                   'out_of_stock': forms.CheckboxInput(),
                   'color': forms.TextInput(attrs=attr.update({'placeholder': 'Color (Optional)'})),
                   'price': MoneyWidget(attrs=attr.update({'placeholder': 'Enter SKU price'})),
                   'size': forms.TextInput(attrs=attr.update({'placeholder': 'Enter SKU size'}))}


ImageFormSet = forms.inlineformset_factory(Product, ImageURL, extra=5, can_delete=False, form=ImageURLForm)
ColorFormSet = forms.inlineformset_factory(Product, ColorURL, extra=4, can_delete=False, form=ColorURLForm)
SkuFormSet = forms.inlineformset_factory(Product, Sku, extra=5, can_delete=False, form=SkuForm)
