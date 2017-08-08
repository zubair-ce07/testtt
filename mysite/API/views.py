from .serializers import BrandSerializer, UserSerializer,\
                                ProductSerializer
from rest_framework import generics
from authentication.models import User
from super_store.models import Brand, Product
from rest_framework import permissions
from .throttling import CustomThrottle
from rest_framework_tracking.mixins import LoggingMixin


class BrandList(generics.ListAPIView):
    throttle_classes = (CustomThrottle,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class BrandCreate(generics.CreateAPIView):

    throttle_classes = (CustomThrottle,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class BrandDetails(LoggingMixin, generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = (CustomThrottle,)

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser
    )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
