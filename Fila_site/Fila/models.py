from django.db import models
from django.db.models import Count, Max


class Product(models.Model):

    retailer_Sku = models.CharField(max_length=50)

    CHOICES = (
        (1, "Men's"),
        (2, "Women's"),
        (3, "Boys"),
        (4, "Girls"),
    )

    gender = models.CharField(max_length = 50, choices = CHOICES, default = "unisex")

    brand = models.CharField(max_length = 50)
    url = models.URLField(max_length = 100)
    name = models.CharField(max_length = 100)
    description = models.CharField(null = True, blank = True, max_length = 1000)
    care = models.CharField(null = True, blank= True,max_length = 1000)
    image_url = models.CharField(max_length = 9000)


class Skus(models.Model):

    retailer_Sku = models.ForeignKey(Product, on_delete = models.CASCADE)
    sku_id = models.CharField(max_length = 1000)
    size = models.CharField(max_length = 50) 
    color = models.CharField(max_length = 100) 
    currency = models.CharField(max_length = 50) 
    price = models.CharField(max_length = 1000)
