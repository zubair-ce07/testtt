from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework import status

from shopcity.models import Product


def _params(request):
    query_params = request.GET
    filtered_params = {
        'brand': query_params.get('Brand', None),
        'size': query_params.get('Size', None),
        'colour': query_params.get('Colour', None),
        'category': query_params.get('Category', None),
        'name': query_params.get('Name', None),
        'minimum_price': query_params.get('Minimum Price', None),
        'maximum_price': query_params.get('Maximum Price', None),
    }
    out_of_stock = query_params.get('Out of Stock', None)
    if out_of_stock == 'false' or out_of_stock == 'true':
        out_of_stock = False if out_of_stock == 'false' else True
    filtered_params['out_of_stock'] = out_of_stock
    return filtered_params


def _q_query(params):
    q = Q()
    if params['out_of_stock'] is not None:
        q = q & Q(out_of_stock=params['out_of_stock'])
    if params["brand"]:
        q = q & Q(brand__iexact=params["brand"])
    if params['size']:
        q = q & Q(skus__size__iexact=params['size'])
    if params['colour']:
        q = q & Q(skus__colour__iexact=params['colour'])
    if params['category']:
        q = q & Q(categories__category__iexact=params['category'])
    if params['name']:
        q = q & Q(name__contains=params['name'])
    if params['maximum_price'] and params['minimum_price']:
        q = q & Q(skus__price__range=(int(params['minimum_price']), int(params['maximum_price'])))
    return q


def _cache_key(params):
    key = ''
    if params['out_of_stock'] is not None:
        key += f"_out_of_stock_{str(params['out_of_stock'])}"
    if params["brand"]:
        key += f"_brand_{params['brand'].lower()}"
    if params['size']:
        key += f"_size_{params['size'].lower()}"
    if params['colour']:
        key += f"_colour_{params['colour'].lower()}"
    if params['category']:
        key += f"_category_{params['category'].lower()}"
    if params['name']:
        key += f"_name_{params['name'].lower()}"
    if params['maximum_price'] and params['minimum_price']:
        key += f"_min_price_{str(params['minimum_price'])}_max_price_{str(params['maximum_price'])}"
    return key


def cached_filtered_products(request):
    params = _params(request)
    cache_key = _cache_key(params)
    query_set = cache.get(f'products_{cache_key}')
    if not query_set:
        q = _q_query(params)
        query_set = Product.objects.prefetch_related('skus').filter(q).distinct()
        cache.set(f'products_{cache_key}', query_set)
    return query_set


def cached_users_queryset():
    queryset = cache.get('users')
    if not queryset:
        queryset = User.objects.all()
        cache.set('users', queryset)
    return queryset


def cached_product(product_id):
    product = cache.get(f'product_{product_id}')
    if not product:
        product = Product.objects.prefetch_related('skus').filter(retailer_sku=product_id)
        if product:
            cache.set(f'product_{product[0].retailer_sku}', product)
    if product:
        return product
    return status.HTTP_404_NOT_FOUND


def cached_user(user_id):
    user = cache.get(f'user_{user_id}')
    if not user:
        user = User.objects.filter(id=user_id)
        if user:
            cache.set(f'user_{user[0].id}', user)
    if user:
        return user
    else:
        status.HTTP_404_NOT_FOUND


def clear_products_cache(kwargs):
    cache.delete_pattern('products_*')
    cache.delete(f'product_{kwargs["instance"].retailer_sku}')


@receiver(post_delete, sender=Product)
def product_post_delete_handler(sender, **kwargs):
    clear_products_cache(kwargs)


@receiver(post_save, sender=Product)
def product_post_save_handler(sender, **kwargs):
    clear_products_cache(kwargs)


def clear_users_cache():
    cache.delete_pattern('users*')


@receiver(post_delete, sender=User)
def user_post_delete_handler(sender, **kwargs):
    clear_users_cache()


@receiver(post_save, sender=User)
def user_post_save_handler(sender, **kwargs):
    if kwargs['created']:
        clear_users_cache()
