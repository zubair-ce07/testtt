import logging

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response

from .models import Author, Book, Category, Publisher
from .utils import regisiter_user

logger = logging.getLogger(__name__)


class AuthorSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},
                                      write_only=True)

    class Meta:
        model = Author
        fields = ['first_name', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
        }

    def save(self):
        return regisiter_user(self.validated_data, Author)


class PublisherSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},
                                      write_only=True)

    class Meta:
        model = Publisher
        fields = ['company_name', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'company_name': {'required': True},
        }

    def save(self):
        return regisiter_user(self.validated_data, Publisher)


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
        ]


class AuthorDataSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id', 'full_name'
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = [
            'id', 'name',
        ]


class PublisherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Publisher
        fields = [
            'id', 'company_name', 'email', 'address', 'website', 'phone',
        ]


class PublisherDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = [
            'id', 'company_name'
        ]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'pages', 'date_published', 'isbn', 'authors',
            'categories', 'publisher'
        ]

        extra_kwargs = {
            'authors': {'required': True},
            'categories': {'required': True},
            'publisher': {'required': True},
        }

    def validate_authors(self, authors):
        if not authors:
            raise serializers.ValidationError(
                {'Atleast one author is required'})

        for author in authors:
            if 'id' not in author:
                raise serializers.ValidationError({'id': 'is required'})

        return authors

    def validate_categories(self, categories):
        if not categories:
            raise serializers.ValidationError(
                {'Atleast one author is required'})

        for category in categories:
            if 'id' not in category:
                raise serializers.ValidationError({'id': 'is required'})

        return categories

    def validate_publisher(self, publisher):
        if not publisher:
            raise serializers.ValidationError({'Publisher is required'})

        return publisher

    @transaction.atomic
    def create(self, validated_data):
        """
        Create a new book instance and associates existing authors, categories
        and publisher
        """
        try:
            authors_data = validated_data.pop('authors')
            categories_data = validated_data.pop('categories')
            publisher_data = validated_data.pop('publisher')

            book = super().create(validated_data)

            publisher = get_object_or_404(Publisher, pk=publisher_data['id'])
            book.publisher = publisher

            Book.update_m2m(authors_data, book.authors)
            Book.update_m2m(categories_data, book.categories)

            return book
        except IntegrityError as exp:
            logging.err(f"Failed to update book, {str(exp)}")
            return book
        return

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Updates m2m relationshiop by adding new assocations and deleting
        old/unwanted assoctions
        """
        try:
            publisher_id = validated_data.pop('publisher')['id']
            publisher = get_object_or_404(Publisher, pk=publisher_id)
            instance.publisher = publisher

            Book.update_m2m(validated_data.pop('authors'), instance.authors)
            Book.update_m2m(validated_data.pop('categories'),
                            instance.categories)

            return super().update(instance, validated_data)

        except IntegrityError as exp:
            logging.error(f"Failed to update book, {str(exp)}")

        return instance
