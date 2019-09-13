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

    template = loader.get_template('Fila/product.html')
    product.image_url = product.image_url.split(',')
    
    context = {
        'product': product,
        'skus': product.skus.all(),
    }

    return HttpResponse(template.render(context, request))
