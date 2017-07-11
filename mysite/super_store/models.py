from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe


class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand_link = models.URLField()
    image_icon = models.ImageField()

    def image_tag(self):
        return mark_safe('<img src="/media/{}" width="150" height="150"/>'\
                         .format(self.image_icon))

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250, verbose_name="Name")
    product_id = models.CharField(max_length=50, verbose_name="Product ID")
    source_url = models.URLField()
    category = models.CharField(max_length=500, null=True, blank=True)
    entry_date = models.DateField(
        default=timezone.now,
        verbose_name='Add Date')
    update_date = models.DateField(
        default=timezone.now,
        verbose_name='Update Date')

    def __str__(self):
        return self.product_id+' '+self.product_name


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return self.product.product_id + 'product\'s image'


class Skus(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20, null=True, blank=True)
    price = models.IntegerField()
    availability = models.BooleanField()

    def __str__(self):
        return self.product.product_id + 'product\'s Sku'


class Menu(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=500, default='')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
