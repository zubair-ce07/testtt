from rest_framework import serializers
from lms.models import Book, Author
from user.serializers import UserDetailSerializer


# Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', )

# Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'summary', 'authors', )

class BookListSerializer(serializers.ModelSerializer):
    author_detail = AuthorSerializer(many=True, read_only=True, source='authors')
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'summary', 'authors', 'author_detail' )
        



