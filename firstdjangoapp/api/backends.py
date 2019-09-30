import coreapi
from django.db.models import Q
from rest_framework.filters import BaseFilterBackend

from shopcity.models import Product


class SimpleFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        query_params = request.GET
        brand = query_params.get('Brand', None)
        size = query_params.get('Size', None)
        colour = query_params.get('Colour', None)
        category = query_params.get('Category', None)
        name = query_params.get('Name', None)
        minimum_price = query_params.get('Minimum Price', None)
        maximum_price = query_params.get('Maximum Price', None)
        out_of_stock = query_params.get('Out of Stock', False)

        if out_of_stock == 'false' or out_of_stock == 'true':
            out_of_stock = False if out_of_stock == 'false' else True
        q = Q(out_of_stock=out_of_stock)
        if brand:
            q = q & Q(brand__iexact=brand)
        if size:
            q = q & Q(skus__size=size)
        if colour:
            q = q & Q(skus__colour=colour)
        if category:
            q = q & Q(categories__category=category)
        if name:
            q = q & Q(name__contains=name)
        if maximum_price and minimum_price:
            q = q & Q(skus__price__range=(int(minimum_price), int(maximum_price)))
        return Product.objects.filter(q).distinct()

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name='Brand',
                location='query',
                required=False,
                type='string',
                description='Brand of the products.'
            ),
            coreapi.Field(
                name='Size',
                location='query',
                required=False,
                type='string',
                description='Size of products.'
            ),
            coreapi.Field(
                name='Colour',
                location='query',
                required=False,
                type='string',
                description='Colour of products.'
            ),
            coreapi.Field(
                name='Category',
                location='query',
                required=False,
                type='string',
                description='Category of products.'
            ),
            coreapi.Field(
                name='Name',
                location='query',
                required=False,
                type='string',
                description='Name of product'

            ),
            coreapi.Field(
                name='Minimum Price',
                location='query',
                required=False,
                type='number',
                description='Minimum price of product'
            ),
            coreapi.Field(
                name='Maximum Price',
                location='query',
                required=False,
                type='number',
                description='Maximum price of product'
            ),
            coreapi.Field(
                name='Out of Stock',
                location='query',
                required=False,
                type='boolean',
                description='Out of stock products'
            ),
        ]
        return fields
