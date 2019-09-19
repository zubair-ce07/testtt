import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from .controller import save_products
from .models import Category, Product, Skus
from users.models import Cart, CartItem


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

        minimum = int(request.GET['minimum']) if request.GET['minimum'] else 0
        maximum = int(request.GET['maximum']) if request.GET['maximum'] else 0
        brand = request.GET['brand']
        size = request.GET['size']
        colour = request.GET['colour']
        category = request.GET['category']
        name = request.GET['name']
        q = Q(out_of_stock=request.GET['out_of_stock'])
        if brand:
            q = q & Q(brand=brand)
        if size:
            q = q & Q(skus__size=size)
        if colour:
            q = q & Q(skus__colour=colour)
        if category:
            q = q & Q(categories__category=category)
        if name:
            q = q & Q(name__contains=name)
        if maximum != 0 or minimum != 0:
            q = q & Q(skus__price__range=(minimum, maximum))
        return Product.objects.filter(q).distinct()

    def get(self, request):
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


class ProductView(View):
    template_name = 'product_detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, retailer_sku=product_id)
        context = product.as_dict()
        context['product'] = product
        return render(request, self.template_name, context)

    def post(self, request, product_id):
        product = get_object_or_404(Product, retailer_sku=product_id)
        if request.user.is_superuser:
            product.skus.filter(sku_id=request.POST['sku_id']).update(out_of_stock=True)
            skus = product.skus.all()
            Product.objects.filter(retailer_sku=product_id).update(
                out_of_stock=all([sku.out_of_stock for sku in skus])
            )
        else:
            if not request.user.cart.filter(state='Current').exists():
                c = Cart(user=request.user, state='Current')
                c.save()
            cart_item = CartItem(
                cart=request.user.cart.get(state='Current'),
                product=product,
                quantity=request.POST['quantity'],
                sku_id=request.POST['sku_id']
            )
            cart_item.save()
        return self.get(request, product_id)
