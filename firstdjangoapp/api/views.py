from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, views
from rest_framework import status
from rest_framework.response import Response

from users.models import Cart, CartItem, Profile
from shopcity.models import Product
from .backends import SimpleFilterBackend
from .redis_cache import (
    cached_product, cached_filtered_products,
    cached_user, cached_users_queryset,
    cached_options
)
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
    lookup_field = 'username'

    def get_queryset(self):
        queryset = cached_user(self.kwargs['username'])
        return queryset

    def partial_update(self, request, *args, **kwargs):
        profile_data = request.data.pop('profile', None)
        carts_data = request.data.pop('cart', None)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if profile_data:
            profile = Profile.objects.get(user=instance)
            profile.address = profile_data.get('address', profile.address)
            profile.state = profile_data.get('state', profile.state)
            profile.city = profile_data.get('city', profile.city)
            profile.zip_code = profile_data.get('zip_code', profile.zip_code)
            profile.contact = profile_data.get('contact', profile.contact)
            profile.save()

        if carts_data:
            for cart_data in carts_data:
                cart_items = cart_data.pop('cart_item', None)
                cart_id = cart_data.get('id', None)
                cart = None
                if cart_id:
                    cart = Cart.objects.get(id=cart_id)
                    cart.state = cart_data.get('state', cart.state)
                else:
                    cart = Cart(user=instance, state=cart_data.get('state'))
                    cart.save()
                if cart_items:
                    for cart_item in cart_items:
                        product = Product.objects.get(retailer_sku=cart_item.get('product'))
                        CartItem.objects.create(
                            cart=cart,
                            product=product,
                            quantity=cart_item.get('quantity'),
                            sku_id=cart_item.get('sku_id')
                        )

        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class OptionsList(views.APIView):

    def get(self, *args, **kwargs):
        options = cached_options()
        return Response(options)
