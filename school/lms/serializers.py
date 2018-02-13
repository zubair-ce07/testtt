from rest_framework import serializers
from lms.models import Book, Author, Bookissue
from user.serializers import UserDetailSerializer


# Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', )



# Book
class BookListSerializer(serializers.ModelSerializer):
    author_detail = AuthorSerializer(many=True, read_only=True, source='authors')
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'summary', 'authors', 'author_detail', 'issued_to' )
        read_only_fields = ('issued_to', )
        

class BookShortDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'summary', )


# BookIssue
class BookissueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bookissue
        fields = ('user', 'book', 'issue_date', 'returned_date')
        

class BookissueListSerializer(serializers.ModelSerializer):
    book_detail = BookShortDetailsSerializer(read_only=True, source='book')
    user_detail = UserDetailSerializer(read_only=True, source='user')
    class Meta:
        model = Bookissue
        fields = ('user', 'user_detail', 'book', 'book_detail', 'issue_date', 'returned_date')
        



