from rest_framework import filters, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from . import models, serializers


class CategoryList(generics.ListAPIView):
    """List all categories."""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDataList(generics.ListAPIView):
    """List all categories name and id with out pagination."""
    pagination_class = None
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    """Get a specific category"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryCreate(generics.CreateAPIView):
    """Create a new category"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = serializers.CategorySerializer


class CategoryDestroy(generics.DestroyAPIView):
    """Delete a specific category"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryUpdate(generics.UpdateAPIView):
    """Updates a specific category"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
