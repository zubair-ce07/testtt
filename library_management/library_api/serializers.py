from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.response import Response

from .models import Author, Book, Category, Publisher
from .utils import regisiter_user

class BaseSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
                                style={'input_type': 'password'},
                                write_only=True
                            )

    class Meta:
        fields = ['username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AuthorSignupSerializer(BaseSignupSerializer):
    class Meta(BaseSignupSerializer.Meta):
        _meta = BaseSignupSerializer.Meta
        model = Author
        fields = _meta.fields + ['first_name']
        extra_kwargs = {
            **_meta.extra_kwargs,
            **{'first_name': {'required': True}}
        }

    def save(self):
        return regisiter_user(self.validated_data, Author)


class PublisherSignupSerializer(BaseSignupSerializer):
    class Meta:
        _meta = BaseSignupSerializer.Meta
        model = Publisher
        fields = _meta.fields + ['company_name']
        extra_kwargs = {
            **_meta.extra_kwargs,
            **{'company_name': {'required': True}}
        }

    def save(self):
        return regisiter_user(self.validated_data, Publisher)


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone'
        ]



class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Category
        fields = [
            'id', 'name',
        ]


class PublisherSerializer(serializers.ModelSerializer):
    # books = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='book-detail'
    # )

    id = serializers.IntegerField(required=False)
    class Meta:
        model = Publisher
        fields = [
            'id', 'company_name', 'address', 'website', 'phone',
        ]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)
    publisher = PublisherSerializer()

    # authors_ids = serializers.PrimaryKeyRelatedField(
    #                             many=True, write_only=True, source='authors',
    #                             queryset=Author.objects.all(),
    #                         )
    # categories_ids = serializers.PrimaryKeyRelatedField(
    #                                 many=True, write_only=True,
    #                                 source='categories',
    #                                 queryset=Category.objects.all(),
    #                             )
    # publisher_id = serializers.PrimaryKeyRelatedField(
    #                                 write_only=True, source='publisher',
    #                                 queryset=Author.objects.all(),
    #                             )

    # serializers.StringRelatedField(many=True)
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'pages', 'date_published', 'isbn', 'authors',
            'categories', 'publisher'
        ]


        # extra_kwargs = {
        #     'id': {'read_only': True},
        #     'authors': {'read_only': True},
        #     'categories': {'read_only': True},
        #     'categories': {'read_only': True}
        # }


    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Updates m3m relationshiop by adding new assocations and deleting
        old/unwanted assoctions
        """
        # import pdb;pdb.set_trace();

        try:
            if 'publisher' in validated_data:
                publisher = validated_data.pop('publisher')
                if 'id' in publisher:
                    pub = Publisher.objects.filter(id=publisher['id']).first()

                    if pub:
                        instance.publisher = pub

            if 'authors' in validated_data:
                Book.update_m2m(
                        validated_data.pop('authors'), instance.authors)

            if 'categories' in validated_data:
                Book.update_m2m(
                        validated_data.pop('categories'), instance.categories)

            return super().update(instance, validated_data)

        except IntegrityError:
            pass
        return ''
