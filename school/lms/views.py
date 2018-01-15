from rest_framework import generics
from lms.models import Book, Author
from lms.serializers import BookSerializer, BookListSerializer, AuthorSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class AuthorList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_url_kwarg = 'author_id'


class BookList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = 'book_id'
