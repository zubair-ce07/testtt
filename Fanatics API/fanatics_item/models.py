from django.db import models


class FanaticsItem(models.Model):
    product_id = models.CharField(primary_key=True, max_length=20)
    breadcrumb = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    brand = models.CharField(max_length=10)
    categories = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True, default='No Description')
    details = models.CharField(max_length=300)
    gender = models.CharField(max_length=20)
    product_url = models.CharField(max_length=100)
    image_urls = models.CharField(max_length=300)
    price = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    language = models.CharField(max_length=20)
    skus = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'FanaticsItem'


