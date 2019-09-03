from .models import Category, Product, Skus


def save_products(raw_products):
    products = []
    categories = []
    skus = []
    for raw_product in raw_products:
        product = _product(raw_product)
        products.append(product)
        categories.extend(_categories(product, raw_product))
        skus.extend(_skus(product, raw_product))
    Product.objects.bulk_create(products)
    Category.objects.bulk_create(categories)
    Skus.objects.bulk_create(skus)


def _product(product_info):
    return Product(
        retailer_sku=product_info['retailer_sku'],
        name=product_info['name'],
        brand=product_info['brand'],
        currency=product_info['currency'],
        price=product_info['price'],
        url=product_info['url'],
        description=';'.join(product_info['description']),
        image_url=";".join(product_info['image_urls']),
        care=";".join(product_info['care']),
        gender=product_info['gender'],
        out_of_stock=_out_of_stock(product_info['skus'])
    )


def _categories(product, product_info):
    return [Category(category=c, product=product) for c in product_info['category']]


def _skus(product, product_info):
    skus = []
    for sku_id, sku_info in product_info['skus'].items():
        skus.append(
            Skus(
                sku_id=sku_id,
                price=sku_info['price'],
                currency=sku_info['currency'],
                size=sku_info['size'],
                colour=sku_info.get('colour', ''),
                previous_prices=":".join(map(str, sku_info['previous_prices'])),
                out_of_stock=sku_info['out_of_stock'],
                product=product
            )
        )
    return skus


def _out_of_stock(skus):
    for sku_id, sku_info in skus.items():
        if not sku_info['out_of_stock']:
            return False
    return True
