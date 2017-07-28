from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import View

from products.forms import CreateProductForm, EditProductForm, ImageFormSet, ColorFormSet, SkuFormSet
from products.models import Product
from products.services import product_load_service


class CreateProductView(LoginRequiredMixin, View):
    form_class = CreateProductForm
    template_name = 'products/create_product.html'

    def get(self, request, *args, **kwargs):
        product = Product()
        form = self.form_class()
        imageformset = ImageFormSet(instance=product)
        colorformset = ColorFormSet(instance=product)
        skuformset = SkuFormSet(instance=product)
        return render(request, self.template_name,
                      {'form': form, 'imageformset': imageformset, 'skuformset': skuformset,
                       'colorformset': colorformset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        imageformset = ImageFormSet(request.POST)
        colorformset = ColorFormSet(request.POST)
        skuformset = SkuFormSet(request.POST)
        if form.is_valid():
            product = form.save()
            imageformset = ImageFormSet(request.POST, instance=product)
            colorformset = ColorFormSet(request.POST, instance=product)
            skuformset = SkuFormSet(request.POST, instance=product)
            if imageformset.is_valid() and colorformset.is_valid() and skuformset.is_valid():
                imageformset.save()
                colorformset.save()
                skuformset.save()
            return redirect('products:search-product')
        return render(request, self.template_name,
                      {'form': form, 'imageformset': imageformset, 'skuformset': skuformset,
                       'colorformset': colorformset})


class EditProductView(LoginRequiredMixin, View):
    form_class = EditProductForm
    template_name = 'products/edit_product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(None, instance=product)
        imageformset = ImageFormSet(None, instance=product)
        colorformset = ColorFormSet(None, instance=product)
        skuformset = SkuFormSet(None, instance=product)
        return render(request, self.template_name,
                      {'form': form, 'imageformset': imageformset, 'colorformset': colorformset,
                       'skuformset': skuformset})

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(request.POST, instance=product)
        if form.is_valid():
            form.save()
            skuformset = SkuFormSet(request.POST, instance=product)
            imageformset = ImageFormSet(request.POST, instance=product)
            colorformset = ColorFormSet(request.POST, instance=product)
            if imageformset.is_valid() and colorformset.is_valid() and skuformset.is_valid():
                imageformset.save()
                colorformset.save()
                skuformset.save()
        return redirect('products:search-product')


class DeleteProductView(LoginRequiredMixin, View):
    template_name = 'products/delete_product.html'

    def get(self, request, *args, **kwargs):
        if Product.objects.filter(pk=kwargs.get('pk')):
            return render(request, self.template_name, {'product': Product.objects.get(pk=kwargs.get('pk'))})
        return redirect('products:search-product')

    def post(self, request, *args, **kwargs):
        if Product.objects.filter(pk=kwargs.get('pk')):
            Product.objects.get(pk=kwargs.get('pk')).delete()
        return redirect(reverse_lazy('products:search-product'))


class SearchProductView(LoginRequiredMixin, View):
    template_name = 'products/search_product.html'

    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            query = request.GET.get('q')
            context = {'query': query, 'error': True}
            if query:
                products = Product.objects.filter(name__icontains=query)
                context['products'] = products
                context['error'] = False
            return render(request, self.template_name, context)
        return render(request, self.template_name, {'products': Product.objects.all()})


class LoadProductsView(LoginRequiredMixin, View):
    template_name = 'products/load_product.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        product_load_service()
        return redirect('products:search-product')
