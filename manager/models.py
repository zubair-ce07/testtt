from django.db import models

from django.utils import timezone

class Product(models.Model):
    """ Field to save product info."""
    CATEGORY_TYPES = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    )
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=200)
    pub_date = models.DateField(default=timezone.now())
    image = models.ImageField(upload_to='manager/images')

    def __str__(self):
        return self.name


class Order(models.Model):
    """ Fields for placing order. """

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=16)
    order_date = models.DateField(default=timezone.now())

    def __str__(self):
        return self.name


class OrderItems(models.Model):
    """ It contains relation of both order and product tables. """

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='products')
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='orders')
    quantity = models.IntegerField()
