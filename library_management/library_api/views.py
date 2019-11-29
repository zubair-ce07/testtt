from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book, Category, Publisher
from .serializers import (AuthorDataSerializer, AuthorSerializer,
                          AuthorSignupSerializer, BookSerializer,
                          CategorySerializer, PublisherDataSerializer,
                          PublisherSerializer, PublisherSignupSerializer)


# Auth views
class BaseSignUpView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                data = serializer.data
                data['id'] = user.id
                token, _ = Token.objects.get_or_create(user=user)
                data['token'] = token.key
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


class LogIn(ObtainAuthToken):
    """Custom login view with extra userinfo"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _created = Token.objects.get_or_create(user=user)

        user_data = {
            'token': token.key,
            "user_id": user.id,
            "username": user.username,
            "role": 'admin'
        }

        author = Author.objects.filter(pk=user.id).first()
        if author:
            user_data['name'] = author.get_full_name()
            user_data['role'] = 'author'
        else:
            publisher = Publisher.objects.filter(pk=user.id).first()
            if publisher:
                user_data['role'] = 'publisher'
                user_data['name'] = publisher.company_name

        return Response(user_data)


# Author Views
class AuthorList(generics.ListAPIView):
    """List all authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', ]


class AuthorDataList(generics.ListAPIView):
    """List all authors full name and id with out pagination."""
    pagination_class = None
    queryset = Author.objects.all()
    serializer_class = AuthorDataSerializer


class AuthorDetail(generics.RetrieveAPIView):
    """Get a specific author"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDestroy(generics.DestroyAPIView):
    """Delete a specific author"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorUpdate(generics.UpdateAPIView):
    """Updates a specific author"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorBooksList(generics.ListAPIView):
    """List all author books."""
    serializer_class = BookSerializer

    def get_queryset(self):
        return Author.objects.get(id=self.kwargs['pk']).books.all()


# Book Views
class BookList(generics.ListAPIView):
    """List all boooks."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title', 'isbn', 'authors__first_name', 'publisher__company_name',
        'categories__name'
    ]


class BookDetail(generics.RetrieveAPIView):
    """Get a specific book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDestroy(generics.DestroyAPIView):
    """Delete a specific book"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdate(APIView):
    """Updates a Book instance."""
    permission_classes = [IsAdminUser, IsAuthenticated]

    def put(self, request, pk, format=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCreate(APIView):
    """ Create a new book."""
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Categiry Views
class CategoryList(generics.ListAPIView):
    """List all categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDataList(generics.ListAPIView):
    """List all categories name and id with out pagination."""
    pagination_class = None
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    """Get a specific category"""
    permission_classes = [IsAuthenticated, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreate(generics.CreateAPIView):
    """Create a new category"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = CategorySerializer


class CategoryDestroy(generics.DestroyAPIView):
    """Delete a specific category"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdate(generics.UpdateAPIView):
    """Updates a specific category"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


# Publisher Views
class PublisherList(generics.ListAPIView):
    """List all publishers."""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name', ]


class PublisherDetail(generics.RetrieveAPIView):
    """Get a specific publisher"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class PublisherDestroy(generics.DestroyAPIView):
    """Delete a specific publisher"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class PublisherUpdate(generics.UpdateAPIView):
    """Updates a specific publisher"""
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class PublisherBooksList(generics.ListAPIView):
    """List all publisher's books."""
    serializer_class = BookSerializer

    def get_queryset(self):
        return Publisher.objects.get(id=self.kwargs['pk']).books.all()


class PublisherDataList(generics.ListAPIView):
    """List all publisher's company name and id with out pagination."""
    pagination_class = None
    queryset = Publisher.objects.all()
    serializer_class = PublisherDataSerializer
