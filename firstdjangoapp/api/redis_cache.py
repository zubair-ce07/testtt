from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from shopcity.models import Product


def cached_products_queryset():
    queryset = cache.get('products')
    if not queryset:
        queryset = Product.objects.all()
        cache.set('products', queryset)
    return queryset


def cached_users_queryset():
    queryset = cache.get('users')
    if not queryset:
        queryset = User.objects.all()
        cache.set('users', queryset)
    return queryset


def clear_products_cache():
    cache.delete('products')


@receiver(post_delete, sender=Product)
def product_post_delete_handler(sender, **kwargs):
    clear_products_cache()


@receiver(post_save, sender=Product)
def product_post_save_handler(sender, **kwargs):
    if kwargs['created']:
        clear_products_cache()


def clear_users_cache():
    cache.delete('users')


@receiver(post_delete, sender=User)
def user_post_delete_handler(sender, **kwargs):
    clear_users_cache()


@receiver(post_save, sender=User)
def user_post_save_handler(sender, **kwargs):
    if kwargs['created']:
        clear_users_cache()
