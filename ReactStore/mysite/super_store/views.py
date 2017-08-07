from django.shortcuts import render
from .models import Brand, Product
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required(login_url=reverse_lazy("authentication:login"))
def display_data(request):
    products = Product.objects.all()
    return render(request, 'super_store/index.html', {'products': products})


class ProductsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("authentication:login")
    model = Product
    template_name = 'super_store/product_list.html'
    items_per_page = 48

    def get_queryset(self):
        product_list = self.model.objects.all()
        try:
            paginator = Paginator(product_list, self.items_per_page)
            page = self.request.GET.get('page', 1)
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return products


class ListBrandProductsView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("authentication:login")
    model = Brand
    template_name = 'super_store/product_list.html'
    items_per_page = 48

    def get_queryset(self):
        try:
            product_list = self.model.objects.get(
                name=self.kwargs['name']).product_set.all()
            paginator = Paginator(product_list, self.items_per_page)
            page = self.request.GET.get('page', 1)
            products = paginator.page(page)

        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = None
        except Brand.DoesNotExist:
            raise Http404("Brand name: {} does not exist".format(
                self.kwargs['name']))
        return products

    def get_context_data(self, **kwargs):
        context = super(ListBrandProductsView, self).get_context_data(**kwargs)
        context['given_brand'] = self.kwargs['name']

        return context


class BrandListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("authentication:login")
    model = Brand
    template_name = 'super_store/brands.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy("authentication:login")
    model = Product
    template_name = 'super_store/product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        context['colors'] = set()
        context['sizes'] = set()
        prod = context['product']
        for sku in prod.skus_set.all():
            context['colors'].add(sku.color)
            context['sizes'].add(sku.size)
        return context
