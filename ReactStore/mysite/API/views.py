from .serializers import BrandSerializer, UserSerializer, ProductSerializer,\
                            BrandOnlySerializer, ProductOnlySerializer
from rest_framework import generics, permissions, authentication
from authentication.models import User
from super_store.models import Brand, Product
from .throttling import CustomThrottle
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BrandList(generics.ListAPIView):
    throttle_classes = (CustomThrottle,)
    queryset = Brand.objects.all()
    serializer_class = BrandOnlySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    pagination_class = StandardResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)


class BrandCreate(generics.CreateAPIView):

    throttle_classes = (CustomThrottle,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    authentication_classes = (authentication.TokenAuthentication,)


class ProductCreate(generics.CreateAPIView):
    throttle_classes = (CustomThrottle,)
    queryset = Product.objects.all()
    serializer_class = ProductOnlySerializer

    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    authentication_classes = (authentication.TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(
            brand=Brand.objects.get(name=self.request.data['name']))


class BrandDetails(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = (CustomThrottle,)
    queryset = Brand.objects.all()
    serializer_class = BrandOnlySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser
    )
    authentication_classes = (authentication.TokenAuthentication,)


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
    pagination_class = StandardResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)


class BrandProductList(generics.ListAPIView):
    throttle_classes = (CustomThrottle,)
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    authentication_classes = (authentication.TokenAuthentication,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        name = self.kwargs['name']
        return Brand.objects.filter(name=name)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    authentication_classes = (authentication.TokenAuthentication,)
