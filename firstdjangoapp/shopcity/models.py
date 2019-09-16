from collections import defaultdict

from django.db import models
from django.conf import settings


class Product(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('AUD', 'Australian Dollar'),
        ('GBP', 'Great Britain Pound'),
    ]
    GENDER_CHOICES = [
        ('women', 'women'),
        ('men', 'men'),
        ('girls', 'girls'),
        ('boys', 'boys'),
        ('unisex-kids', 'unisex-kids'),
        ('unisex-adults', 'unisex-adults'),
    ]
    retailer_sku = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200)
    brand = models.CharField(blank=True, max_length=50)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    price = models.IntegerField()
    url = models.URLField()
    description = models.TextField(blank=True)
    image_url = models.TextField()
    care = models.TextField(blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    out_of_stock = models.BooleanField()

    def __str__(self):
        return self.retailer_sku

    def as_dict(self, *args, **kwargs):
        categories = self.categories.all()
        skus = self.skus.all()
        colours_and_sizes = defaultdict(lambda: [])
        for sku in skus:
            colours_and_sizes[sku.colour].append([sku.size, sku.out_of_stock])
        return {
            'images': self.image_url.split(';'),
            'description': self.description.split(';'),
            'care': [c for c in self.care.split(';') if c],
            'colours_and_sizes': dict(colours_and_sizes),
            'categories': categories[:settings.NUMBER_OF_CATEGORIES_BREADCRUMB]
        }


class Category(models.Model):
    category = models.CharField(blank=True, max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.category


class Skus(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('AUD', 'Australian Dollar'),
        ('GBP', 'Great Britain Pound'),
    ]
    sku_id = models.CharField(max_length=50)
    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES)
    colour = models.CharField(blank=True, max_length=20)
    price = models.IntegerField()
    size = models.CharField(blank=True, max_length=20)
    previous_prices = models.TextField(blank=True)
    out_of_stock = models.BooleanField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="skus")

    def __str__(self):
        return self.sku_id
