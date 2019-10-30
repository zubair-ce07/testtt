from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Product
from .forms import ProductsAction
from users.models import ProductForm


class Home(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'index.html', {'user': request.user, 'products':products})

    def post(self, request):
        form = ProductsAction(request.POST)
        if form.is_valid():
            if 'delete' in request.POST:
                for item in request.POST.getlist('choices'):
                    Product.objects.filter(id=item).delete()
            if 'price' in request.POST:
                for item in request.POST.getlist('choices'):
                    Product.objects.filter(id=item).update(price=request.POST.get('price'))

        return render(request, 'index.html')

class AddProduct(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'add_product.html', {'product_form': form})

    def post(self, request):
        if request.method == "POST":
            name = request.POST['name']
            price = request.POST['price']
            description = request.POST['description']
            category = request.POST['category']
            pub_date = request.POST['pub_date']
            image = request.POST['image']

            if Product.objects.filter(name=name).exists():
                Product.objects.filter(name=name).update(price=price, \
                    description=description, category=category, image=image, \
                    pub_date=pub_date)
            else:
                product = Product(name=name, price=price, category=category, \
                description=description, image=image, pub_date=pub_date)
                product.save()
        return render(request, 'add_product.html')
