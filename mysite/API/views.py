from .serializers import BrandSerializer, CustomUserSerializer
from rest_framework import generics
from authentication.models import CustomUser
from super_store.models import Brand, Product,  Images, Skus
from rest_framework import permissions
from .throttling import MyCustomThrottle
from rest_framework_tracking.mixins import LoggingMixin


class BrandList(generics.ListCreateAPIView):
    throttle_classes = (MyCustomThrottle,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
