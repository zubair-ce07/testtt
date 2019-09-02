from django.db import models


class Product(models.Model):
    CURRENCY_CHOICES = [
        ('USD', "US_Dollar"),
        ('EUR', "Euro"),
        ('AUD', 'Australian_Dollar'),
        ('GBP', 'Great Britain Pound'),
    ]
    retailer_sku = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)
    brand = models.CharField(blank=True, max_length=50)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    price = models.IntegerField()
    url = models.URLField()
    description = models.TextField(blank=True)
    image_url = models.TextField()
    care = models.TextField(blank=True)
    gender = models.CharField(max_length=20)
    previous_prices = models.TextField(blank=True)
    out_of_stock = models.BooleanField()

    def __str__(self):
        return self.retailer_sku


class Category(models.Model):
    category = models.CharField(blank=True, max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.product.retailer_sku


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
        return self.product.retailer_sku
