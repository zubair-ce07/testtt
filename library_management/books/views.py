from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


class BookList(generics.ListAPIView):
    """List all books."""
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title', 'isbn', 'authors__first_name', 'publisher__company_name',
        'categories__name'
    ]


class BookDetail(generics.RetrieveAPIView):
    """Get a specific book"""
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookDestroy(generics.DestroyAPIView):
    """Delete a specific book"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookUpdate(APIView):
    """Updates a Book instance."""
    permission_classes = [IsAdminUser, IsAuthenticated]

    def put(self, request, pk, format=None):
        book = get_object_or_404(models.Book, pk=pk)
        serializer = serializers.BookSerializer(
            book, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCreate(APIView):
    """ Create a new book."""
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request, format=None):
        serializer = serializers.BookSerializer(
            data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
