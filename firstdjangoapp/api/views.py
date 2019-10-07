from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .backends import SimpleFilterBackend
from .redis_cache import cached_product, cached_filtered_products, cached_user, cached_users_queryset
from .serializers import ProductSerializer, UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ProductList(generics.ListCreateAPIView):
    filter_backends = (SimpleFilterBackend,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        return cached_filtered_products(self.request)


@method_decorator(csrf_exempt, name='dispatch')
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'retailer_sku'

    def get_queryset(self):
        product = cached_product(self.kwargs['retailer_sku'])
        return product


@method_decorator(csrf_exempt, name='dispatch')
class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return cached_users_queryset()

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = cached_user(self.kwargs['id'])
        return queryset
