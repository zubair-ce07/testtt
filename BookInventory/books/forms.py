from django.forms import ModelForm
from books.models import Author, Book, Publisher


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'publisher', 'authors', 'pub_date']


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'address', 'contact', 'email', 'city', 'country']


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'contact', 'email', 'city', 'country']
