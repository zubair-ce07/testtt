from django.db import models


class Product(models.Model):
    retailer_sku = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)
    brand = models.CharField(blank=True, max_length=50)
    currency = models.CharField(max_length=10)
    price = models.IntegerField()
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.retailer_sku


class Category(models.Model):
    category = models.CharField(blank=True, max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.retailer_sku


class Description(models.Model):
    description = models.CharField(blank=True, max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.retailer_sku


class ImageUrls(models.Model):
    image_url = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.retailer_sku


class Skus(models.Model):
    sku_id = models.CharField(primary_key=True, max_length=20)
    currency = models.CharField(max_length=10)
    colour = models.CharField(blank=True, max_length=20)
    price = models.IntegerField()
    size = models.CharField(blank=True, max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.retailer_sku


class Care(models.Model):
    care = models.CharField(blank=True, max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.retailer_sku
