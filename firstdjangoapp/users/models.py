from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from phone_field import PhoneField

from shopcity.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=50)
    contact = PhoneField(null=True)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"{self.user} Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity = models.IntegerField()
    sku_id = models.CharField(max_length=50)
    sku_price = models.IntegerField()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
