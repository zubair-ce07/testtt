from django.db import models


class FanaticsItem(models.Model):
    product_id = models.CharField(primary_key=True, max_length=20)
    breadcrumb = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    brand = models.CharField(max_length=10)
    categories = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='No Description')
    details = models.TextField()
    gender = models.CharField(max_length=10)
    product_url = models.URLField(max_length=300)
    image_urls = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=10)
    language = models.CharField(max_length=10)
    skus = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'FanaticsItem'
