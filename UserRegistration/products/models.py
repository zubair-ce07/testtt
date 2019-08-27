from django.db import models

GENDER_MAP = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('U', 'UNISEX'),
        ('K', 'KIDS')
    )


class Brand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=600)
    gender = models.CharField(max_length=4, choices=GENDER_MAP)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    url = models.URLField()


class ProductArticle(models.Model):
    product = models.ForeignKey(Product, related_name='articles', on_delete=models.CASCADE)
    color = models.CharField(max_length=30)
    price = models.FloatField()
    size = models.CharField(max_length=15)

