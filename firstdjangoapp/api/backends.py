import coreapi
from rest_framework.filters import BaseFilterBackend


class SimpleFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset

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
