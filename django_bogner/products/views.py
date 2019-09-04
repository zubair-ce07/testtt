from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product, Image


class IndexView(generic.ListView):
    template_name = 'products/index.html'
    context_object_name = 'category_list'
    paginate_by = 24

    def get_queryset(self):
        return Category.objects.all()


class CategoryProducts(generic.ListView):
    template_name = 'products/category_products.html'
    context_object_name = 'product_list'
    paginate_by = 24
    model = Product

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryProducts, self).get_context_data(**kwargs)
        context['category_name'] = (Category.objects.get(pk=self.kwargs['pk'])).category_name
        return context


class ProductDetail(LoginRequiredMixin, generic.DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['skus'] = (Product.objects.get(pk=self.kwargs['pk'])).sku_set.all()
        context['image_urls'] = Image.objects.filter(product=self.kwargs['pk'])
        return context
