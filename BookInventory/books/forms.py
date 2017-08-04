from django.forms import ModelForm

from books.models import Author, Book, Publisher


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'
