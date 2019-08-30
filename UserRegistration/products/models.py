from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    url = models.URLField()


class ProductArticle(models.Model):
    product = models.ForeignKey(Product, related_name='articles', on_delete=models.CASCADE)
    color = models.CharField(max_length=200)
    price = models.FloatField()
    size = models.CharField(max_length=100)

