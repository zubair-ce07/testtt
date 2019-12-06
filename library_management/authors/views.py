from rest_framework import filters, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from books.serializers import BookSerializer

from . import models, serializers


# Author Views
class AuthorList(generics.ListAPIView):
    """List all authors."""
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', ]


class AuthorDataList(generics.ListAPIView):
    """List all authors full name and id with out pagination."""
    pagination_class = None
    queryset = models.Author.objects.all()
    serializer_class = serializers.CustomAuthorSerializer


class AuthorDetail(generics.RetrieveAPIView):
    """Get a specific author"""
    permission_classes = [IsAuthenticated]
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class AuthorDestroy(generics.DestroyAPIView):
    """Delete a specific author"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class AuthorUpdate(generics.UpdateAPIView):
    """Updates a specific author"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class AuthorBooksList(generics.ListAPIView):
    """List all author books."""
    serializer_class = BookSerializer

    def get_queryset(self):
        return models.Author.objects.get(id=self.kwargs['pk']).books.all()
