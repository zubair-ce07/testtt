from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from phone_field import PhoneField

from shopcity.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=50)
    contact = PhoneField(null=True)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    STATE_CHOICES = [
        ('Current', 'Current'),
        ('Processed', 'Processed'),
        ('Canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    state = models.CharField(max_length=20, choices=STATE_CHOICES)

    def __str__(self):
        return f"{self.user} Cart"

    def as_dict(self):
        cart_items = self.cart_items.all()
        cart_total = 0
        for cart_item in cart_items:
            cart_total += (cart_item.product.skus.get(sku_id=cart_item.sku_id).price * cart_item.quantity)
        context = {
            "cart_items": cart_items,
            "number_of_products": cart_items.aggregate(Sum('quantity'))['quantity__sum'],
            "cart_total": cart_total
        }
        return context


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_products")
    quantity = models.IntegerField()
    sku_id = models.CharField(max_length=50)
