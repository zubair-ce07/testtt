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
            product = self.product(prod)
            product_objs.append(product)
            category_objs.extend(self.categories(product, prod))
            sku_objs.extend(self.skus(product, prod))
        Product.objects.bulk_create(product_objs)
        Category.objects.bulk_create(category_objs)
        Skus.objects.bulk_create(sku_objs)

    def product(self, product_info):
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
            previous_prices=';'.join(map(str, product_info['previous_prices'])),
            out_of_stock=self.out_of_stock(product_info['skus'])
        )

    def categories(self, product, product_info):
        return [Category(
            category=c,
            product=product
        )
            for c in product_info['category']]

    def skus(self, product, product_info):
        return [Skus(
            sku_id=sku_id,
            price=sku_info['price'],
            currency=sku_info['currency'],
            size=sku_info['size'],
            colour=sku_info.get('colour', ''),
            previous_prices=":".join(map(str, sku_info['previous_prices'])),
            out_of_stock=sku_info['out_of_stock'],
            product=product
        )
            for sku_id, sku_info in product_info['skus'].items()]

    def out_of_stock(self, skus):
        for sku_id, sku_info in skus.items():
            if not sku_info['out_of_stock']:
                return False
        return True
