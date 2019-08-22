from django.shortcuts import render
from json import load
from .models import Product, Category, Description, Skus, ImageUrls, Care


def upload_file(request):
    if request.method == 'POST':
        handle_file(request.FILES['fileToUpload'])
    return render(request, "uploadfiles/uploadfile.html", {})


def handle_file(f):
    with open(f.temporary_file_path()) as json_file:
        products = load(json_file)
        save_products_to_database(products)


def save_products_to_database(products):
    for prod in products:
        product = Product()
        product.retailer_sku = prod['retailer_sku']
        product.currency = prod['currency']
        product.price = prod['price']
        product.brand = prod['brand']
        product.name = prod['name']
        product.url = prod['url']
        product.save()

        for c in prod['category']:
            category = Category()
            category.category = c
            category.product = product
            category.save()

        for d in prod['description']:
            description = Description()
            description.description = d
            description.product = product
            description.save()

        for img_url in prod['image_urls']:
            image_urls = ImageUrls()
            image_urls.image_url = img_url
            image_urls.product = product
            image_urls.save()

        for c in prod['care']:
            care = Care()
            care.care = c
            care.product = product
            care.save()

        for sku_id, sku_info in prod['skus'].items():
            sku = Skus()
            sku.sku_id = sku_id
            sku.price = sku_info['price']
            sku.currency = sku_info['currency']
            sku.size = sku_info['size']
            sku.colour = sku_info.get('colour', '')
            sku.product = product
            sku.save()
        print(f"inserted: {product.retailer_sku}")
