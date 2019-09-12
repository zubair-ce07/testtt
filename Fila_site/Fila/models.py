from django.db import models
from django.db.models import Count, Max


class Product(models.Model):
    Retailer_Sku = models.CharField(max_length=50)
    Gender = models.CharField(max_length = 50)
    Brand = models.CharField(max_length = 50)
    Url = models.CharField(max_length = 100)
    Name = models.CharField(max_length = 100)
    Description = models.CharField(null = True, blank= True, max_length = 1000)
    Care = models.CharField(null = True, blank= True,max_length = 1000)
    Image_url = models.CharField(max_length = 9000)


class Skus(models.Model):
    Retailer_Sku = models.ForeignKey(Product,on_delete = models.CASCADE)
    Sku_id = models.CharField(max_length = 1000)
    Size = models.CharField(max_length = 50) 
    Color = models.CharField(max_length = 100) 
    Currency = models.CharField(max_length = 50) 
    Price = models.CharField(max_length = 1000)

