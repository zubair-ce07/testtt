from books.models import Book, RequestBook, IssueBook
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Book
        fields = ['url', 'id', 'title', 'author_name', 'publisher', 'number_of_books']

class RequestBookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RequestBook
        fields = ['id', 'user', 'book']

class IssueBookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IssueBook
        fields = ['id', 'user', 'book', 'issue_date', 'return_date']

