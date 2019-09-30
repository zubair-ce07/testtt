from rest_framework import generics

from .backends import SimpleFilterBackend
from .permissions import AllowAnyOrAdmin, IsLoggedInUserOrAdmin, IsAdmin, ReadOnly
from .redis_cache import cached_products_queryset, cached_product, cached_user, cached_users_queryset
from .serializers import ProductSerializer, UserSerializer


class ProductList(generics.ListCreateAPIView):
    filter_backends = (SimpleFilterBackend,)
    permission_classes = [IsAdmin | ReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return cached_products_queryset()


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
