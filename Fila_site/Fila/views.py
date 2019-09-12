from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.template import loader

from .models import Product, Skus

# Create your views here.


def home(request): 

    products = Product.objects.all()[:1000]

    for product in products:
            product.Image_url = product.Image_url.split(',')        
    
    template = loader.get_template('Fila/home.html')

    context = {
        'products': products,
    }

    return HttpResponse(template.render(context, request))

def product_detail(request,id):

    product = Product.objects.get(id = id)
    skus_list = Skus.objects.all()

    skus = []

    for sku in skus_list:
        if int(sku.Retailer_Sku.id) == int(id):
            skus.append(sku)


    template = loader.get_template('Fila/product.html')
    product.Image_url = product.Image_url.split(',')
    
    context = {
        'product': product,
        'skus': skus,
    }

    return HttpResponse(template.render(context, request))

