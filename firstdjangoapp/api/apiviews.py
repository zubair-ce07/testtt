from django.contrib.auth.models import User
from rest_framework import generics

from shopcity.models import Product
from .permissions import AllowAnyOrAdmin, IsLoggedInUserOrAdmin, IsAdmin, ReadOnly
from .redis_cache import cache_products_queryset, cache_users_queryset
from .serializers import ProductSerializer, UserSerializer


class ProductList(generics.ListCreateAPIView):
    permission_classes = [IsAdmin | ReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return cache_products_queryset()


class ProductDetail(generics.RetrieveAPIView):
    permission_classes = [IsAdmin | ReadOnly]
    serializer_class = ProductSerializer
    lookup_field = 'retailer_sku'

    def get_queryset(self):
        queryset = Product.objects.filter(retailer_sku=self.kwargs['retailer_sku'])
        return queryset


class UserList(generics.ListCreateAPIView):
    permission_classes = [AllowAnyOrAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        return cache_users_queryset()


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [IsLoggedInUserOrAdmin]
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = User.objects.filter(id=self.kwargs['id'])
        return queryset
