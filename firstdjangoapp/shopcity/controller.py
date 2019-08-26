from json import load

from .models import (
    Category,
    Product,
    Skus
)


class Controller:
    def handle_file(self, file):
        with open(file.temporary_file_path()) as json_file:
            try:
                products = load(json_file)
                self.save_products_to_database(products)
                return True
            except ValueError:
                return False

    def save_products_to_database(self, products):
        product_objs = []
        category_objs = []
        sku_objs = []
        for prod in products:
            product = Product(
                retailer_sku=prod['retailer_sku'],
                name=prod['name'],
                brand=prod['brand'],
                currency=prod['currency'],
                price=prod['price'],
                url=prod['url'],
                description=';'.join(prod['description']),
                image_url=";".join(prod['image_urls']),
                care=";".join(prod['care']),
                gender=prod['gender'],
                previous_prices=';'.join(map(str, prod['previous_prices']))
            )
            product_objs.append(product)
            category_objs.extend(
                [Category(category=c, product=product)
                 for c in prod['category']]
            )
            sku_objs.extend(
                [Skus(
                    sku_id=sku_id,
                    price=sku_info['price'],
                    currency=sku_info['currency'],
                    size=sku_info['size'],
                    colour=sku_info.get('colour', ''),
                    previous_prices=":".join(map(str, sku_info['previous_prices'])),
                    out_of_stock=sku_info['out_of_stock'],
                    product=product
                )
                    for sku_id, sku_info in prod['skus'].items()]
            )
        Product.objects.bulk_create(product_objs)
        Category.objects.bulk_create(category_objs)
        Skus.objects.bulk_create(sku_objs)
