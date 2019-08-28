from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=25)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    url = models.CharField(max_length=1000)
    retailer_sku = models.CharField(max_length=15)
    category = models.ManyToManyField(Category)
    brand = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = ArrayField(models.CharField(max_length=700))
    care = ArrayField(models.CharField(max_length=700))
    image_urls = ArrayField(models.CharField(max_length=1000))
    market = models.CharField(max_length=10)
    retailer = models.CharField(max_length=30)
    skus = ArrayField(JSONField(null=True, blank=True), blank=True, null=True)
    price = models.IntegerField()
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.retailer_sku
