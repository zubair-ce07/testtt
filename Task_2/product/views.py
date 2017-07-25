from django.shortcuts import render, redirect
from django.views.generic.edit import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from product.models import Product, ImageURL, SKU, ColorURL
from product.forms import CreateProductForm, EditProductForm, ImageFormSet, ColorFormSet, skuFormSet


class CreateProductView(LoginRequiredMixin, View):
    form_class = CreateProductForm
    template_name = 'product/create_product.html'

    def get(self, request, *args, **kwargs):
        product = Product()
        form = self.form_class()
        imageformset = ImageFormSet(instance=product)
        colorformset = ColorFormSet(instance=product)
        skuformset = skuFormSet(instance=product)
        return render(request, self.template_name,
                      {'form': form, 'imageformset': imageformset, 'skuformset': skuformset,
                       'colorformset': colorformset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            product = form.save()
            skuformset = skuFormSet(request.POST, instance=product)
            imageformset = ImageFormSet(request.POST, instance=product)
            colorformset = ColorFormSet(request.POST, instance=product)
            if imageformset.is_valid() and colorformset.is_valid() and skuformset.is_valid():
                imageformset.save()
                colorformset.save()
                skuformset.save()
        return redirect('product:search-product')


class EditProductView(LoginRequiredMixin, View):
    form_class = EditProductForm
    template_name = 'product/edit_product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(None, instance=product)
        imageformset = ImageFormSet(None, instance=product)
        colorformset = ColorFormSet(None, instance=product)
        skuformset = skuFormSet(None, instance=product)
        return render(request, self.template_name,
                      {'form': form, 'imageformset': imageformset, 'colorformset': colorformset,
                       'skuformset': skuformset})

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(request.POST, instance=product)
        if form.is_valid():
            form.save()
            skuformset = skuFormSet(request.POST, instance=product)
            imageformset = ImageFormSet(request.POST, instance=product)
            colorformset = ColorFormSet(request.POST, instance=product)
            if imageformset.is_valid() and colorformset.is_valid() and skuformset.is_valid():
                imageformset.save()
                colorformset.save()
                skuformset.save()
        return redirect('product:search-product')


class DeleteProductView(LoginRequiredMixin, View):
    template_name = 'product/delete_product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        return render(request, self.template_name, {'product': product})

    def post(self, request, *args, **kwargs):
        Product.objects.get(pk=kwargs.get('pk')).delete()
        return redirect(reverse_lazy('product:search-product'))


class SearchProductView(LoginRequiredMixin, View):
    template_name = 'product/search_product.html'

    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            query = request.GET.get('q')
            context = {'query': query, 'error': True}
            if query:
                products = Product.objects.filter(name__icontains=query)
                context['products'] = products
                context['error'] = False
            return render(request, self.template_name, context)
        return render(request, self.template_name)
