import json
from itertools import islice

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
            brand, _ = Brand.objects.get_or_create(name=brand)
            category, _ = Category.objects.get_or_create(name=category)
            product, _ = Product.objects.get_or_create(
                name=name,
                brand=brand,
                category=category,
                description=description
            )
            self.save_images(product, images)
            self.save_articles(product, articles)
        self.stdout.write(self.style.SUCCESS("Products Loaded"))

    @staticmethod
    def save_images(product, images):
        batch_size = len(images)
        product_images = (ProductImage(url=image, product=product) for image in images)
        batch = list(islice(product_images, batch_size))
        ProductImage.objects.bulk_create(batch, batch_size)

    @staticmethod
    def save_articles(product, articles):
        batch_size = len(articles)
        product_articles = (ProductArticle(
            color=article['color'],
            price=article['price'],
            size=article['size'],
            product=product
        ) for article in articles.values())
        batch = list(islice(product_articles, batch_size))
        ProductImage.objects.bulk_create(batch, batch_size)

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        self.save_product(path)

