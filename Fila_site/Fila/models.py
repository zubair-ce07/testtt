from django.db import models
from django.db.models import Count, Max


class Product(models.Model):

    retailer_sku = models.CharField(max_length=50)

    CHOICES = (
        (1, "Men's"),
        (2, "Women's"),
        (3, "Boys"),
        (4, "Girls"),
    )

    gender = models.CharField(max_length = 50, choices = CHOICES, default = CHOICES)

    brand = models.CharField(max_length = 50)
    url = models.URLField(max_length = 100)
    name = models.CharField(max_length = 100)
    description = models.TextField(blank=True, null=True)
    care = models.TextField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)



class Skus(models.Model):

    retailer_Sku = models.ForeignKey(Product, on_delete = models.CASCADE)
    sku_id = models.CharField(max_length = 1000)
    size = models.CharField(max_length = 50) 
    color = models.CharField(max_length = 100) 
    currency = models.CharField(max_length = 50) 
    price = models.CharField(max_length = 1000)
