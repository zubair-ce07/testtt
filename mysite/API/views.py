from .serializers import BrandSerializer, CustomUserSerializer,\
    ProductSerializer, ImageSerializer, SkuSerializer, ProductCreateSerializer
from rest_framework import generics
from authentication.models import CustomUser
from super_store.models import Brand, Product,  Images, Skus
from rest_framework import permissions
from .throttling import MyCustomThrottle
from rest_framework_tracking.mixins import LoggingMixin


class BrandList(generics.ListAPIView):
    throttle_classes = (MyCustomThrottle,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class BrandCreate(generics.CreateAPIView):
    throttle_classes = (MyCustomThrottle,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class BrandDetails(LoggingMixin, generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = (MyCustomThrottle,)

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser
    )


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class ProductCreate(generics.CreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
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


# class ImageList(generics.ListCreateAPIView):
#     queryset = Images.objects.all()
#     serializer_class = ImageSerializer
#     permission_classes = (
#         permissions.IsAuthenticated,
#         permissions.IsAdminUser,
#     )


# class ImageDetial(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Images.objects.all()
#     serializer_class = ImageSerializer
#     permission_classes = (
#         permissions.IsAuthenticated,
#         permissions.IsAdminUser,
#     )


# class SkuList(generics.ListCreateAPIView):
#     queryset = Skus.objects.all()
#     serializer_class = SkuSerializer
#     permission_classes = (
#         permissions.IsAuthenticated,
#         permissions.IsAdminUser,
#     )


# class SkuDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Skus.objects.all()
#     serializer_class = SkuSerializer
#     permission_classes = (
#         permissions.IsAuthenticated,
#         permissions.IsAdminUser,
#     )
