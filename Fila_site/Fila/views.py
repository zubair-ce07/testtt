from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.template import loader

from .models import Product, Skus

def home(request): 

    products = Product.objects.all()[:1000]

    for product in products:
            product.image_url = product.image_url.split(',')        
    
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
        if int(sku.retailer_Sku.id) == int(id):
            skus.append(sku)


    template = loader.get_template('Fila/product.html')
    product.image_url = product.image_url.split(',')
    
    context = {
        'product': product,
        'skus': skus,
    }

    return HttpResponse(template.render(context, request))
