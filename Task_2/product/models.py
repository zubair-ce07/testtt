from django.db import models
from djmoney.models.fields import MoneyField


class Product(models.Model):
    url = models.URLField()
    retailer_sku = models.BigIntegerField()
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    fabric = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'


class ImageURL(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField()


class sku(models.Model):
    out_of_stock = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, unique=True, max_length=15)
    color = models.CharField(max_length=10)
    price = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR')


class ColorURL(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField()
