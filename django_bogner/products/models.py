from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=1000, blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    gender_choices = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
        ('Unisex', 'Unisex')
    ]

    url = models.URLField(max_length=400)
    retailer_sku = models.CharField(max_length=30, unique=True)
    category = models.ManyToManyField(Category, related_name='products')
    brand = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=gender_choices, default='Unisex')
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=1000, blank=True)
    description = models.TextField()
    care = models.TextField()
    market = models.CharField(max_length=20)
    retailer = models.CharField(max_length=30)
    price = models.IntegerField()
    currency = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.retailer_sku} - {self.url}"


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku_id = models.CharField(max_length=100)
    price = models.IntegerField()
    currency = models.CharField(max_length=10)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    out_of_stock = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.sku_id}"


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1000, unique=True)

    def __str__(self):
        return self.image_url
