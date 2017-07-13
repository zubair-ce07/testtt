from .serializers import BrandSerializer, CustomUserSerializer
from rest_framework import generics
from authentication.models import CustomUser
from super_store.models import Brand, Product,  Images, Skus
from rest_framework import permissions



class BrandList(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BrandDetails(generics.RetrieveUpdateDestroyAPIView):
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
