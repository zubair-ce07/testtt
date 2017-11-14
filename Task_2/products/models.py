from django.db import models
from djmoney.models.fields import MoneyField


class Product(models.Model):
    url = models.URLField()
    retailer_sku = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    fabric = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '{}_{}'.format(self.retailer_sku, self.name)

    class Meta:
        db_table = 'product'


class ImageURL(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return '{}, {}'.format(self.product.name, self.url)

    class Meta:
        db_table = 'image_url'


class ColorURL(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return '{}, {}'.format(self.product.name, self.url)

    class Meta:
        db_table = 'color_url'


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=3)
    color = models.CharField(max_length=10, blank=True, null=True)
    price = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR')
    out_of_stock = models.BooleanField(default=False)

    def __str__(self):
        return '{}_{}'.format(self.product.retailer_sku, self.size)

    class Meta:
        db_table = 'sku'


class DateTime(models.Model):
    datetime = models.DateTimeField()
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return str(self.datetime)

    class Meta:
        db_table = 'datetime'
