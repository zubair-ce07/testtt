import json
from collections import defaultdict

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View

from .controller import save_products
from .models import Category, Product, Skus


class FileUpload(View):
    template_name = "uploadfile.html"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        json_file = request.FILES['jsonfile']
        with open(json_file.temporary_file_path()) as json_file:
            try:
                raw_products = json.load(json_file)
            except ValueError:
                return HttpResponse('Invalid File!!')
            else:
                save_products(raw_products)
                return HttpResponse('Successfully inserted!!')


class ProductSearch(View):
    template_name = "productsearch.html"
    context = {
        "brand_choices": sorted(list(Product.objects.values_list('brand', flat=True).distinct())),
        "size_choices": sorted(list(Skus.objects.values_list('size', flat=True).distinct())),
        "colour_choices": sorted(list(Skus.objects.values_list('colour', flat=True).distinct())),
        "category_choices": sorted(list(Category.objects.values_list('category', flat=True).distinct()))
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class ResultsBaseView(View):
    template_name = "viewresults.html"

    def get_queryset(self, request, *args, **kwargs):
        pass

    def get(self, request):
        product_list = self.get_queryset(request)
        paginator = Paginator(product_list, 20)
        page = request.GET.get('page', 1)
        products = paginator.get_page(page)
        context = {
            "products": products
        }
        return render(request, self.template_name, context)


class ViewResults(ResultsBaseView):

    def get_queryset(self, request, *args, **kwargs):
        brand = request.GET['brand'] if request.GET['brand'] != 'All' else None
        size = request.GET['size'] if request.GET['size'] != 'All' else None
        colour = request.GET['colour'] if request.GET['colour'] != 'All' else None
        category = request.GET['category'] if request.GET['category'] != 'All' else None
        minimum = request.GET['minimum'] if request.GET['minimum'] != '' else 0
        maximum = request.GET['maximum'] if request.GET['maximum'] != '' else 0
        name = request.GET['name'] if request.GET['name'] != '' else None
        out_of_stock = True if request.GET['out_of_stock'] == 'Yes' else False

        products = Product.objects.filter(Q(out_of_stock=out_of_stock))
        if brand:
            products = products.filter(Q(brand=brand))
        if size:
            products = products.filter(Q(skus__size=size))
        if colour:
            products = products.filter(Q(skus__colour=colour)).distinct()
        if category:
            products = products.filter(Q(categories__category=category))
        if name:
            products = products.filter(Q(name__contains=name))
        if int(maximum) != 0 and int(minimum) <= int(maximum):
            products = products.filter(Q(price__range=(request.GET.get('minimum'), request.GET.get('maximum'))))
        return products


class ViewAllProducts(ResultsBaseView):

    def get_queryset(self, request, *args, **kwargs):
        return Product.objects.filter(Q(out_of_stock=False))


class ViewProduct(View):
    template_name = "product_detail.html"

    def get(self, request):
        if 'id' not in request.GET:
            raise Http404
        product = Product.objects.get(Q(retailer_sku=request.GET.get('id')))
        product.clean_fields()
        skus = product.skus.all()
        categories = product.categories.all()
        colours_and_sizes = defaultdict(lambda: [])

        for sku in skus:
            colours_and_sizes[sku.colour].append([sku.size, sku.out_of_stock])

        context = {
            'product': product,
            'colours_and_sizes': dict(colours_and_sizes),
            'images': product.image_url,
            'description': product.description,
            'care': product.care,
            'categories': categories[:1]
        }
        return render(request, self.template_name, context)
