from .serializers import BrandSerializer, UserSerializer, ProductSerializer
from rest_framework import generics, permissions, authentication
from authentication.models import User
from super_store.models import Brand, Product
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
    authentication_classes = (authentication.TokenAuthentication,)


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


class ProductList(generics.ListAPIView):
    throttle_classes = (CustomThrottle,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    authentication_classes = (authentication.TokenAuthentication,)


class BrandProductList(generics.ListAPIView):
    throttle_classes = (CustomThrottle,)
    serializer_class = ProductSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        name = self.kwargs['name']
        return Brand.objects.get(name=name).product_set.all()


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )

    authentication_classes = (authentication.TokenAuthentication,)
