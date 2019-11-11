from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book, Category, Publisher
from .serializers import AuthorSignupSerializer, BookSerializer, PublisherSignupSerializer


class BaseSignUpView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                data = serializer.data
                data['id'] = user.id
                data['token'] = Token.objects.get(user=user).key
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                errors = "Invalid signup class"
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorSignup(BaseSignUpView):
    serializer_class = AuthorSignupSerializer


class PubliserSignup(BaseSignUpView):
    serializer_class = PublisherSignupSerializer


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class BookDetail(APIView):
    """
    Retrieve, update or delete a Book instance.
    """
    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        # import pdb; pdb.set_trace()

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookList(APIView):
    """List all books, or create a new book."""
    def get_queryset(self):
        return Book.objects.all()

    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        # import pdb; pdb.set_trace()

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
