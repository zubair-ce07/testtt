import json

from django.core.management.base import BaseCommand

from products.models import Brand, Category, Product, ProductArticle, ProductImage


class Command(BaseCommand):
    help = "Import Products."

    def save_product(self, path):
        with open(path, 'r') as product_file:
            products = json.load(product_file)

        for product in products:
            name = product['name']
            brand = product['brand']
            category = product['category']
            description = product['description']
            images = product['img_urls']
            articles = product['skus']
            brand = Brand.objects.get_or_create(name=brand)[0]
            category = Category.objects.get_or_create(name=category)[0]
            product = Product.objects.get_or_create(
                name=name,
                brand=brand,
                category=category,
                description=description
            )[0]
            self.save_images(product, images)
            self.save_articles(product, articles)
        self.stdout.write(self.style.SUCCESS("Products Loaded"))

    @staticmethod
    def save_images(product, images):
        for image in images:
            ProductImage.objects.get_or_create(
                url=image,
                product=product
            )

    @staticmethod
    def save_articles(product, articles):
        for article in articles.values():
            ProductArticle.objects.get_or_create(
                color=article['color'],
                price=article['price'],
                size=article['size'],
                product=product
            )

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        self.save_product(path)

