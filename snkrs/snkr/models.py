from django.db import models


class Snkr(models.Model):
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    retailer_sku = models.IntegerField()
    url = models.URLField(max_length=150)

    def __str__(self):
        return f'{self.brand}'


class ImageUrls(models.Model):
    url = models.URLField(max_length=150)
    image_product = models.ForeignKey(
        Snkr,
        related_name="snkr_images",
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.url}'


class Skus(models.Model):
    sku = models.TextField(max_length=200)
    sku_product = models.ForeignKey(
        Snkr,
        related_name="snkr_skus",
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sku}'


class Description(models.Model):
    description = models.TextField(max_length=500)
    product_description = models.ForeignKey(
        Snkr, related_name="snkr_descriptions", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.description}'
