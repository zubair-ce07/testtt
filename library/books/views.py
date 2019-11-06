from books.models import Book, RequestBook, IssueBook
from books.serializers import BookSerializer, IssueBookSerializer, RequestBookSerializer
from rest_framework import generics
from books.permissions import IsLibrarianOrReadOnly, IsOwnerOrReadOnly, IsOwnerLibrarianOrReadOnly
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
        'requestbook': reverse('requestbook-list', request=request, format=format),
        'issuebook': reverse('issuebook-list', request=request, format=format)
    })


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsLibrarianOrReadOnly]

class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsLibrarianOrReadOnly]


class RequestBookList(generics.ListCreateAPIView):
    queryset = RequestBook.objects.all()
    serializer_class = RequestBookSerializer


class RequestBookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RequestBook.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsLibrarianOrReadOnly]

class IssueBookList(generics.ListCreateAPIView):
    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerLibrarianOrReadOnly]

class IssueBookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                    IsOwnerLibrarianOrReadOnly]