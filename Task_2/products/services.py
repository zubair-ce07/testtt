import json

from djmoney.money import Money

from products.models import Product


def product_load_service():
    with open('products.json') as test:
        data = json.load(test)
    for key, value in data.items():
        p = Product.objects.create(url=value.get('url'), retailer_sku=value.get('retailer_sku'),
                                   name=value.get('name')[0],
                                   brand=value.get('brand'), description=value.get('description'),
                                   fabric=value.get('care')[0])
        for url in value.get('image_urls'):
            p.imageurl_set.create(url=url)
        for url in value.get('color_urls'):
            p.colorurl_set.create(url=url)
        for sku in value.get('skus').values():
            p.sku_set.create(color=sku.get('color'), size=sku.get('size'),
                             price=Money(sku.get('price'), sku.get('currency')))
    return data
