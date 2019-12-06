from rest_framework import filters, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from books.serializers import BookSerializer

from . import models, serializers


class PublisherList(generics.ListAPIView):
    """List all publishers."""
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PublisherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name', ]


class PublisherDetail(generics.RetrieveAPIView):
    """Get a specific publisher"""
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PublisherSerializer


class PublisherDestroy(generics.DestroyAPIView):
    """Delete a specific publisher"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PublisherSerializer


class PublisherUpdate(generics.UpdateAPIView):
    """Updates a specific publisher"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PublisherSerializer


class PublisherBooksList(generics.ListAPIView):
    """List all publisher's books."""
    serializer_class = BookSerializer

    def get_queryset(self):
        return models.Publisher.objects.get(id=self.kwargs['pk']).books.all()


class PublisherDataList(generics.ListAPIView):
    """List all publisher's company name and id with out pagination."""
    pagination_class = None
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.CustomPublisherSerializer
