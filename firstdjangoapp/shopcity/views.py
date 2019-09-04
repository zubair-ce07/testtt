import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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


class ViewResults(View):
    template_name = "viewresults.html"

    def get_queryset(self, request, *args, **kwargs):
        if not request.GET or (len(request.GET) == 1 and 'page' in request.GET.keys()):
            return Product.objects.filter(Q(out_of_stock=False))

        minimum = request.GET['minimum'] if request.GET['minimum'] else 0
        maximum = request.GET['maximum'] if request.GET['maximum'] else 0
        q = Q(out_of_stock=request.GET['out_of_stock'])
        if request.GET['brand']:
            q.add(Q(brand=request.GET['brand']), Q.AND)
        if request.GET['size']:
            q.add(Q(skus__size=request.GET['size']), Q.AND)
        if request.GET['colour']:
            q.add(Q(skus__colour=request.GET['colour']), Q.AND)
        if request.GET['category']:
            q.add(Q(categories__category=request.GET['category']), Q.AND)
        if request.GET['name']:
            q.add(Q(name__contains=request.GET['name']), Q.AND)
        if int(maximum) != 0 and int(minimum) <= int(maximum):
            q.add(Q(skus__price__range=(minimum, maximum)), Q.AND)
        return Product.objects.filter(q).distinct()

    def get(self, request):
        if len(request.GET) == 1 and 'id' in request.GET.keys():
            product = get_object_or_404(Product, retailer_sku=request.GET.get('id'))
            context = product.as_dict()
            context['product'] = product
            return render(request, "product_detail.html", context)

        product_list = self.get_queryset(request)
        paginator = Paginator(product_list, 20)
        page = request.GET.get('page', 1)
        products = paginator.get_page(page)
        context = {
            "products": products,
            "brand_choices": list(Product.objects.values_list('brand', flat=True).distinct().order_by('brand')),
            "size_choices": list(Skus.objects.values_list('size', flat=True).distinct().order_by('size')),
            "colour_choices": list(Skus.objects.values_list('colour', flat=True).distinct().order_by('colour')),
            "category_choices": list(Category.objects.values_list(
                'category',
                flat=True
            ).distinct().order_by('category'))
        }
        return render(request, self.template_name, context)
