from django.db.models import Q
from rest_framework import generics

from .backends import SimpleFilterBackend
from .permissions import AllowAnyOrAdmin, IsLoggedInUserOrAdmin, IsAdmin, ReadOnly
from .redis_cache import cached_product, cached_filter_products, cached_user, cached_users_queryset
from .serializers import ProductSerializer, UserSerializer


class ProductList(generics.ListCreateAPIView):
    filter_backends = (SimpleFilterBackend,)
    permission_classes = [IsAdmin | ReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):
        query_params = self.request.GET
        brand = query_params.get('Brand', None)
        size = query_params.get('Size', None)
        colour = query_params.get('Colour', None)
        category = query_params.get('Category', None)
        name = query_params.get('Name', None)
        minimum_price = query_params.get('Minimum Price', None)
        maximum_price = query_params.get('Maximum Price', None)
        out_of_stock = query_params.get('Out of Stock', None)
        q = Q()
        if out_of_stock == 'false' or out_of_stock == 'true':
            out_of_stock = False if out_of_stock == 'false' else True
        if out_of_stock is not None:
            q = q & Q(out_of_stock=out_of_stock)
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
        return cached_filter_products(q)


class ProductDetail(generics.RetrieveAPIView):
    permission_classes = [IsAdmin | ReadOnly]
    serializer_class = ProductSerializer
    lookup_field = 'retailer_sku'

    def get_queryset(self):
        product = cached_product(self.kwargs['retailer_sku'])
        return product


class UserList(generics.ListCreateAPIView):
    permission_classes = [AllowAnyOrAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        return cached_users_queryset()


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [IsLoggedInUserOrAdmin]
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = cached_user(self.kwargs['id'])
        return queryset
